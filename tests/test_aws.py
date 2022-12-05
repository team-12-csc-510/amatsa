import boto3
import pytest
import sure  # type: ignore
from botocore.exceptions import ClientError
from mock import MagicMock, patch
from moto import mock_ses

from src.aws.client.ses import SES


@patch("src.aws.client.ses.SES.send_mail")
def test_send_email(send_mail: MagicMock):
    ses_client = SES(["test@example.com"])
    ses_client.send_mail()
    assert send_mail.called


@mock_ses
def test_service_verify_email_identity():
    conn = boto3.client("ses", region_name="us-east-1")
    conn.verify_email_identity(EmailAddress="test@example.com")

    identities = conn.list_identities()
    address = identities["Identities"][0]
    address.should.equal("test@example.com")


@mock_ses
def test_service_verify_email_identity_idempotency():
    conn = boto3.client("ses", region_name="us-east-1")
    address = "test@example"
    conn.verify_email_identity(EmailAddress=address)
    conn.verify_email_identity(EmailAddress=address)

    identities = conn.list_identities()
    address_list = identities["Identities"]
    address_list.should.equal([address])


@mock_ses
def test_service_verify_email_address():
    conn = boto3.client("ses", region_name="us-east-1")
    conn.verify_email_address(EmailAddress="test@example.com")
    email_addresses = conn.list_verified_email_addresses()
    email = email_addresses["VerifiedEmailAddresses"][0]
    email.should.equal("test@example.com")


@mock_ses
def test_service_delete_identity():
    conn = boto3.client("ses", region_name="us-east-1")
    conn.verify_email_identity(EmailAddress="test@example.com")

    conn.list_identities()["Identities"].should.have.length_of(1)
    conn.delete_identity(Identity="test@example.com")
    conn.list_identities()["Identities"].should.have.length_of(0)


@mock_ses
def test_service_send_email():
    conn = boto3.client("ses", region_name="us-east-1")

    kwargs = dict(
        Source="test@example.com",
        Destination={
            "ToAddresses": ["test_to@example.com"],
            "CcAddresses": ["test_cc@example.com"],
            "BccAddresses": ["test_bcc@example.com"],
        },
        Message={
            "Subject": {"Data": "test subject"},
            "Body": {"Text": {"Data": "test body"}},
        },
    )
    conn.send_email.when.called_with(**kwargs).should.throw(ClientError)

    conn.verify_domain_identity(Domain="example.com")
    conn.send_email(**kwargs)

    too_many_addresses = list(f"to{i}@example.com" for i in range(51))
    conn.send_email.when.called_with(
        **dict(kwargs, Destination={"ToAddresses": too_many_addresses})
    ).should.throw(ClientError)

    send_quota = conn.get_send_quota()
    sent_count = int(send_quota["SentLast24Hours"])
    sent_count.should.equal(3)


@mock_ses
def test_service_send_email_invalid_address():
    conn = boto3.client("ses", region_name="us-east-1")
    conn.verify_domain_identity(Domain="example.com")

    with pytest.raises(ClientError) as ex:
        conn.send_email(
            Source="test@example.com",
            Destination={
                "ToAddresses": ["test_to@example.com", "invalid_address"],
                "CcAddresses": [],
                "BccAddresses": [],
            },
            Message={
                "Subject": {"Data": "test subject"},
                "Body": {"Text": {"Data": "test body"}},
            },
        )
    err = ex.value.response["Error"]
    err["Code"].should.equal("InvalidParameterValue")
    err["Message"].should.equal("Missing domain")
