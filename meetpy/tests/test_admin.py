import pytest
from tests.factories import TalkProposalFactory, TalkFactory

@pytest.mark.django_db
def test_if_proposal_is_included_on_the_talk_admin_page(admin_client, db):

    talk_proposal = TalkProposalFactory(talk=TalkFactory())
    response = admin_client.get(f'/admin/meetups/talk/{talk_proposal.id}/change/')
    content = response.content.decode("utf-8")
    assert response.status_code == 200
    assert str(talk_proposal.date_submitted) in content
    assert talk_proposal.message in content
