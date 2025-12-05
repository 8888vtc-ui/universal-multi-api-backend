"""
Tests pour le service Vidéo IA
"""
import pytest
from services.video.queue_manager import VideoQueue
from services.video.storage_manager import VideoStorage
import os
import tempfile
import shutil


@pytest.fixture
def temp_storage():
    """Créer un répertoire temporaire pour stockage"""
    temp_dir = tempfile.mkdtemp()
    storage = VideoStorage(base_path=temp_dir)
    yield storage
    
    # Nettoyer
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)


class TestQueueManager:
    """Tests pour VideoQueue"""
    
    def test_add_to_queue(self):
        """Test ajout à la queue"""
        queue = VideoQueue()
        video_id = "test_video_123"
        queue.add_to_queue(
            video_id=video_id,
            status="processing",
            provider="d-id"
        )
        
        assert video_id in queue.queue
        assert queue.queue[video_id]["status"] == "processing"
    
    def test_get_status(self):
        """Test obtention statut"""
        queue = VideoQueue()
        video_id = "test_video_456"
        queue.add_to_queue(
            video_id=video_id,
            status="processing"
        )
        
        status = queue.get_status(video_id)
        assert status is not None
        assert status["status"] == "processing"
        assert status["video_id"] == video_id
    
    def test_update_status(self):
        """Test mise à jour statut"""
        queue = VideoQueue()
        video_id = "test_video_789"
        queue.add_to_queue(video_id, status="processing")
        
        queue.update_status(video_id, status="done", result_url="http://example.com/video.mp4")
        status = queue.get_status(video_id)
        assert status["status"] == "done"
        assert status["result_url"] == "http://example.com/video.mp4"
    
    def test_get_queue_stats(self):
        """Test statistiques queue"""
        queue = VideoQueue()
        queue.add_to_queue("video1", status="processing")
        queue.add_to_queue("video2", status="done")
        
        stats = queue.get_queue_stats()
        assert stats["total"] == 2
        assert "processing" in stats["by_status"]
        assert "done" in stats["by_status"]


class TestStorageManager:
    """Tests pour VideoStorage"""
    
    def test_save_video_info(self, temp_storage):
        """Test sauvegarde info vidéo"""
        video_id = "test_video_123"
        
        result = temp_storage.save_video_info(
            video_id=video_id,
            provider="d-id",
            video_url="http://example.com/video.mp4"
        )
        
        assert result["video_id"] == video_id
        assert result["provider"] == "d-id"
        assert "created_at" in result
    
    def test_get_video_info(self, temp_storage):
        """Test obtention info vidéo"""
        video_id = "test_video_456"
        
        temp_storage.save_video_info(
            video_id=video_id,
            provider="d-id"
        )
        info = temp_storage.get_video_info(video_id)
        
        assert info is not None
        assert info["video_id"] == video_id
        assert info["provider"] == "d-id"
    
    def test_get_storage_stats(self, temp_storage):
        """Test statistiques stockage"""
        temp_storage.save_video_info("video1", provider="d-id")
        temp_storage.save_video_info("video2", provider="d-id")
        
        stats = temp_storage.get_storage_stats()
        assert "total_videos" in stats
        assert "total_size_mb" in stats
        assert isinstance(stats["total_videos"], int)
        assert stats["total_videos"] >= 2
