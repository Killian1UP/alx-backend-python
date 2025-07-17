#!/usr/bin/env python3

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    @parameterized.expand([
        ("google", {"name": "Google"}),
        ("abc", {"name": "ABC"})
    ])
    @patch("client.get_json")
    def test_org(self, org, expected_data, mock_get_json):
        mock_get_json.return_value = expected_data
        
        client = GithubOrgClient(org)
        result = client.org
        
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org}")
        self.assertEqual(result, expected_data)
    
    def test_public_repos_url(self):
        with patch.object(GithubOrgClient, "org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "https://api.github.com/orgs/google/repos"}
            
            client = GithubOrgClient("google")
            result = client._public_repos_url
            
            self.assertEqual(result, "https://api.github.com/orgs/google/repos")