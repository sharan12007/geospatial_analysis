"""
OAuth2 Authentication Module for Google Earth Engine
"""

import ee
import json
from typing import Optional, Dict, Any
import os


class GEEAuthenticator:
    """
    Handles OAuth2 authentication with Google Earth Engine
    """
    
    def __init__(self, client_id: str = None, client_secret: str = None, service_account_email: str = None):
        """
        Initialize the authenticator with OAuth2 credentials
        
        Args:
            client_id: OAuth2 Client ID for Google Earth Engine
            client_secret: OAuth2 Client Secret (optional for some auth flows)
            service_account_email: Service account email for authentication
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.service_account_email = service_account_email
        self.credentials = None
        
    def authenticate(self, service_account_key_path: Optional[str] = None, project: str = None) -> bool:
        """
        Authenticate with Google Earth Engine using OAuth2 or service account
        
        Args:
            service_account_key_path: Path to service account JSON key file
            project: Google Cloud Project ID
            
        Returns:
            bool: True if authentication successful, False otherwise
        """
        try:
            # Try to get project from environment or use default
            if not project:
                project = os.getenv('GEE_PROJECT', 'earthengine-pipeline')  # Use the correct project
            
            if service_account_key_path and os.path.exists(service_account_key_path):
                # Use service account authentication
                credentials = ee.ServiceAccountCredentials(
                    email=self.service_account_email, 
                    key_file=service_account_key_path
                )
                ee.Initialize(credentials, project=project)
                print("✅ Authenticated with Google Earth Engine using service account")
            elif self.service_account_email:
                # Try to authenticate with service account email (if key is in default location)
                try:
                    credentials = ee.ServiceAccountCredentials(
                        email=self.service_account_email
                    )
                    ee.Initialize(credentials, project=project)
                    print("✅ Authenticated with Google Earth Engine using service account email")
                except:
                    # Fallback to OAuth2
                    ee.Initialize(project=project)
                    print("✅ Authenticated with Google Earth Engine using OAuth2")
            else:
                # Use OAuth2 authentication
                ee.Initialize(project=project)
                print("✅ Authenticated with Google Earth Engine using OAuth2")
            
            # Test the connection
            test_image = ee.Image('USGS/SRTMGL1_003')
            test_value = test_image.getInfo()
            print("✅ Connection test successful")
            return True
            
        except Exception as e:
            print(f"❌ Authentication failed: {str(e)}")
            print("💡 Make sure you have run 'earthengine authenticate' or have proper credentials")
            print(f"💡 Try setting the GEE_PROJECT environment variable to your project ID")
            return False
    
    def get_authentication_code(self) -> str:
        """
        Generate authentication code for the current session
        
        Returns:
            str: Authentication code snippet for use in scripts
        """
        return f"""
# Google Earth Engine Authentication
import ee

# Initialize Earth Engine
ee.Initialize()

# Your OAuth2 Client ID: {self.client_id}
# Note: Make sure you have authenticated using 'earthengine authenticate' command
# or have set up service account credentials
"""
    
    def check_authentication_status(self) -> bool:
        """
        Check if currently authenticated with GEE
        
        Returns:
            bool: True if authenticated, False otherwise
        """
        try:
            # Try to access a simple dataset
            test_image = ee.Image('USGS/SRTMGL1_003')
            test_image.getInfo()
            return True
        except:
            return False
