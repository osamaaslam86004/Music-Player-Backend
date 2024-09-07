# import pytest
# from unittest.mock import patch
# from fastapi.testclient import TestClient
# from sqlalchemy.exc import OperationalError
# from main import app  # Update this with your FastAPI app import

# client = TestClient(app)


# @pytest.mark.asyncio
# async def test_get_audio_tracks_db_connection_error():
#     with pytest.raises(OperationalError):
#         # Mock the `db.execute` method to raise `OperationalError`
#         with patch(
#             "play_music_track.routers.upload.db.execute", side_effect=OperationalError
#         ):
#             response = client.get("/tracks")
#             assert response.status_code == 503
#             assert response.json() == {
#                 "detail": "Database connection lost. Please try again later."
#             }
