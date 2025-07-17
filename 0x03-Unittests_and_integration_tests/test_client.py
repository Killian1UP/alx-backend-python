#!/usr/bin/env python3
"""
Unit tests for GithubOrgClient class in client.py.
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos
import requests
from itertools import cycle


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for methods in GithubOrgClient."""

    @parameterized.expand([
        ("google", {"name": "Google"}),
        ("abc", {"name": "ABC"})
    ])
    @patch("client.get_json")
    def test_org(self, org, expected_data, mock_get_json):
        """Test that GithubOrgClient.org returns the correct org data."""
        mock_get_json.return_value = expected_data
        client = GithubOrgClient(org)
        result = client.org
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org}"
        )
        self.assertEqual(result, expected_data)

    def test_public_repos_url(self):
        """Test that _public_repos_url returns correct repos_url."""
        with patch.object(
            GithubOrgClient, "org", new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/google/repos"
            }
            client = GithubOrgClient("google")
            result = client._public_repos_url
            self.assertEqual(
                result, "https://api.github.com/orgs/google/repos"
            )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns list of repository names."""
        fake_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": {"key": "mit"}},
        ]
        mock_get_json.return_value = fake_payload
        with patch.object(
            GithubOrgClient, "_public_repos_url", new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = "http://awge.url"
            client = GithubOrgClient("google")
            result = client.public_repos()
            expected = ["repo1", "repo2", "repo3"]
            self.assertEqual(result, expected)
            mock_get_json.assert_called_once_with("http://awge.url")
            mock_url.assert_called_once()
            
    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that has_license returns the correct boolean."""
        client = GithubOrgClient("google")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)

@parameterized_class([{
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected": expected_repos,
        "apache2": apache2_repos,
}])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test for GithubOrgClient.public_repos()."""
    
    
    @classmethod
    def setUpClass(cls):
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()         
        mock_get.return_value.json.side_effect = cycle([
           cls.org_payload,
           cls.repos_payload,
        ])
        
    
    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()
        
    def test_public_repos(self):
        client = GithubOrgClient("google")
        result = client.public_repos()
        self.assertEqual(result, self.expected)
        
    def test_public_repos_with_license(self):
        """Test public_repos with license filter 'apache-2.0'."""
        client = GithubOrgClient("google")
        result = client.public_repos(license="apache-2.0")
        self.assertEqual(result, self.apache2)

