import logging
from uuid import UUID
from typing import List
from api.endpoints.models.credentials import PresentCredentialProtocolType

from sqlalchemy.ext.asyncio import AsyncSession


from api.endpoints.models.v1.verifier import (
    PresentationRequestItem,
    CreatePresentationRequestPayload,
)


from api.db.models.v1.verification_request import VerificationRequest


logger = logging.getLogger(__name__)


def v_presentation_request_to_item(
    db_item: PresentationRequestItem,
) -> PresentationRequestItem:
    """IssuerCredential to IssuerCredentialItem.

    Transform a IssuerCredential Table record to a IssuerCredentialItem object.

    Args:
      db_item: The Traction database IssuerCredential
      acapy: When True, populate the IssuerCredentialItem acapy field.

    Returns: The Traction IssuerCredentialItem

    """

    logger.warn(db_item.__dict__)
    item = PresentationRequestItem(
        **db_item.dict(),
    )
    logger.warn(item)
    return item


async def make_presentation_request(
    db: AsyncSession,
    tenant_id: UUID,
    wallet_id: UUID,
    protocol: PresentCredentialProtocolType,
    payload: CreatePresentationRequestPayload,
) -> PresentationRequestItem:
    db_item = VerificationRequest(
        tenant_id=tenant_id,
        contact_id=payload.contact_id,
        status="pending",
        state="pending",
        protocol=protocol,
        role="verifier",
        proof_request=payload.proof_request.dict(),
    )
    db.add(db_item)
    await db.commit()

    return v_presentation_request_to_item(db_item)


async def list_presentation_requests(
    db: AsyncSession,
    tenant_id: UUID,
    wallet_id: UUID,
) -> List[PresentationRequestItem]:

    items = await VerificationRequest.list_by_tenant_id(db, tenant_id)

    return items, len(items)
