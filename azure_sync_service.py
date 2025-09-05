import os
import streamlit as st
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError

def push_to_azure(connection_string, project_root, doc_folder):
    """Pushes the contents of the doc folder to Azure Blob Storage."""
    if not all([connection_string, project_root, doc_folder]):
        st.error("Configuration is missing. Please save the configuration first.")
        return

    try:
        # Sanitize project name for container
        project_name = os.path.basename(project_root).lower().replace(" ", "-")
        container_name = f"fyiai-{project_name}"

        # Create a blob service client
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        # Create container if it doesn't exist
        try:
            container_client = blob_service_client.create_container(container_name)
            st.info(f"Container '{container_name}' created.")
        except ResourceExistsError:
            container_client = blob_service_client.get_container_client(container_name)
            st.info(f"Container '{container_name}' already exists.")

        st.info(f"Starting upload of files from '{doc_folder}' to container '{container_name}'...")

        # Walk through the doc folder and upload files
        files_uploaded_count = 0
        for root, dirs, files in os.walk(doc_folder):
            for file_name in files:
                local_path = os.path.join(root, file_name)
                # Create a blob path that preserves the relative structure
                relative_path = os.path.relpath(local_path, doc_folder)
                # Azure blob storage uses forward slashes
                blob_path = relative_path.replace(os.sep, '/')

                blob_client = container_client.get_blob_client(blob_path)

                with st.spinner(f"Uploading {blob_path}..."):
                    with open(local_path, "rb") as data:
                        blob_client.upload_blob(data, overwrite=True)
                files_uploaded_count += 1

        st.success(f"✅ Push to Azure complete! {files_uploaded_count} files uploaded.")

    except Exception as e:
        st.error(f"An error occurred during push to Azure: {e}")

def pull_from_azure(connection_string, project_root, doc_folder):
    """Pulls the contents of a container from Azure Blob Storage to the doc folder."""
    if not all([connection_string, project_root, doc_folder]):
        st.error("Configuration is missing. Please save the configuration first.")
        return

    try:
        # Sanitize project name for container
        project_name = os.path.basename(project_root).lower().replace(" ", "-")
        container_name = f"fyiai-{project_name}"

        # Create a blob service client
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        container_client = blob_service_client.get_container_client(container_name)

        # Check if container exists
        if not container_client.exists():
            st.error(f"Container '{container_name}' does not exist. Nothing to pull.")
            return

        st.info(f"Starting download of files from container '{container_name}' to '{doc_folder}'...")

        blob_list = container_client.list_blobs()
        files_downloaded_count = 0

        for blob in blob_list:
            blob_client = container_client.get_blob_client(blob.name)

            # Construct local path
            local_path = os.path.join(doc_folder, blob.name.replace('/', os.sep))

            # Create local directories if they don't exist
            os.makedirs(os.path.dirname(local_path), exist_ok=True)

            with st.spinner(f"Downloading {blob.name}..."):
                with open(local_path, "wb") as download_file:
                    download_file.write(blob_client.download_blob().readall())
            files_downloaded_count += 1

        st.success(f"✅ Pull from Azure complete! {files_downloaded_count} files downloaded.")
        # Rerun to refresh the file browser
        st.rerun()

    except Exception as e:
        st.error(f"An error occurred during pull from Azure: {e}")
