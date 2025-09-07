import unittest
from unittest.mock import patch, MagicMock, mock_open
import os

# Since the functions use streamlit for messaging, we need to mock it.
# We'll create a mock streamlit module.
# This needs to be done before importing the service.
st_mock = MagicMock()
patcher = patch.dict('sys.modules', {'streamlit': st_mock})
patcher.start()

from azure_sync_service import push_to_azure, pull_from_azure
from azure.core.exceptions import ResourceExistsError

class TestAzureSyncService(unittest.TestCase):

    def setUp(self):
        """Reset mocks before each test."""
        st_mock.reset_mock()

    @patch('azure_sync_service.BlobServiceClient')
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open, read_data=b'test data')
    def test_push_to_azure_success(self, mock_file, mock_walk, MockBlobServiceClient):
        """Test successful push to Azure."""
        # Setup mocks
        mock_walk.return_value = [
            ('/docs', ('subdir',), ('file1.md',)),
            ('/docs/subdir', (), ('file2.md',)),
        ]

        mock_blob_service_client = MockBlobServiceClient.from_connection_string.return_value
        mock_container_client = mock_blob_service_client.create_container.return_value
        mock_blob_client = mock_container_client.get_blob_client.return_value

        # Call the function
        push_to_azure('conn_str', '/project', '/docs')

        # Assertions
        MockBlobServiceClient.from_connection_string.assert_called_once_with('conn_str')
        mock_blob_service_client.create_container.assert_called_once_with('fyiai-project')

        self.assertEqual(mock_container_client.get_blob_client.call_count, 2)
        mock_container_client.get_blob_client.assert_any_call('file1.md')
        mock_container_client.get_blob_client.assert_any_call('subdir/file2.md')

        self.assertEqual(mock_blob_client.upload_blob.call_count, 2)
        st_mock.success.assert_called_once_with('✅ Push to Azure complete! 2 files uploaded.')

    @patch('azure_sync_service.BlobServiceClient')
    def test_push_to_azure_missing_config(self, MockBlobServiceClient):
        """Test push with missing configuration."""
        push_to_azure('', '/project', '/docs')
        st_mock.error.assert_called_once_with("Configuration is missing. Please save the configuration first.")
        MockBlobServiceClient.from_connection_string.assert_not_called()

    @patch('azure_sync_service.BlobServiceClient')
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open, read_data=b'test data')
    def test_push_to_azure_container_exists(self, mock_file, mock_walk, MockBlobServiceClient):
        """Test push when the container already exists."""
        mock_walk.return_value = [('/docs', (), ('file1.md',))]

        mock_blob_service_client = MockBlobServiceClient.from_connection_string.return_value
        mock_blob_service_client.create_container.side_effect = ResourceExistsError("Container already exists")

        # Call the function
        push_to_azure('conn_str', '/project', '/docs')

        # Assertions
        mock_blob_service_client.create_container.assert_called_once()
        mock_blob_service_client.get_container_client.assert_called_once_with('fyiai-project')
        st_mock.success.assert_called_once()

    @patch('azure_sync_service.BlobServiceClient')
    @patch('os.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    def test_pull_from_azure_success(self, mock_file, mock_makedirs, MockBlobServiceClient):
        """Test successful pull from Azure."""
        # Setup mocks
        mock_blob_service_client = MockBlobServiceClient.from_connection_string.return_value
        mock_container_client = mock_blob_service_client.get_container_client.return_value
        mock_container_client.exists.return_value = True

        mock_blob1 = MagicMock()
        mock_blob1.name = 'file1.md'
        mock_blob2 = MagicMock()
        mock_blob2.name = 'subdir/file2.md'

        mock_container_client.list_blobs.return_value = [mock_blob1, mock_blob2]

        mock_blob_client = mock_container_client.get_blob_client.return_value
        mock_blob_client.download_blob.return_value.readall.return_value = b'downloaded data'

        # Call the function
        pull_from_azure('conn_str', '/project', '/docs')

        # Assertions
        self.assertEqual(mock_makedirs.call_count, 2)
        mock_makedirs.assert_any_call(os.path.join('/docs'), exist_ok=True)
        mock_makedirs.assert_any_call(os.path.join('/docs', 'subdir'), exist_ok=True)


        self.assertEqual(mock_file.call_count, 2)
        mock_file().write.assert_any_call(b'downloaded data')

        st_mock.success.assert_called_once_with('✅ Pull from Azure complete! 2 files downloaded.')
        st_mock.rerun.assert_called_once()

    @patch('azure_sync_service.BlobServiceClient')
    def test_pull_from_azure_container_does_not_exist(self, MockBlobServiceClient):
        """Test pull when the container does not exist."""
        mock_blob_service_client = MockBlobServiceClient.from_connection_string.return_value
        mock_container_client = mock_blob_service_client.get_container_client.return_value
        mock_container_client.exists.return_value = False

        pull_from_azure('conn_str', '/project', '/docs')

        st_mock.error.assert_called_once_with("Container 'fyiai-project' does not exist. Nothing to pull.")

    @patch('azure_sync_service.BlobServiceClient')
    def test_pull_from_azure_missing_config(self, MockBlobServiceClient):
        """Test pull with missing configuration."""
        pull_from_azure('conn_str', '', '/docs')
        st_mock.error.assert_called_once_with("Configuration is missing. Please save the configuration first.")
        MockBlobServiceClient.from_connection_string.assert_not_called()

# This allows running the tests directly from the command line
if __name__ == '__main__':
    # Stop the patcher after tests are done
    try:
        unittest.main()
    finally:
        patcher.stop()
