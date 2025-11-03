"""
Comprehensive tests for .gitignore configuration.
"""

import os
import re
import unittest
from pathlib import Path


class TestGitignore(unittest.TestCase):
    """Test suite for .gitignore file validation."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.project_root = Path(__file__).parent.parent
        cls.gitignore_path = cls.project_root / ".gitignore"
        
        with open(cls.gitignore_path, 'r', encoding='utf-8') as f:
            cls.gitignore_content = f.read()
            cls.gitignore_lines = [
                line.strip() for line in cls.gitignore_content.splitlines()
                if line.strip() and not line.strip().startswith('#')
            ]

    def test_gitignore_exists(self):
        """Test that .gitignore exists."""
        self.assertTrue(
            self.gitignore_path.exists(),
            ".gitignore should exist in project root"
        )

    def test_gitignore_not_empty(self):
        """Test that .gitignore is not empty."""
        self.assertTrue(
            len(self.gitignore_lines) > 0,
            ".gitignore should not be empty"
        )

    def test_gitignore_has_python_patterns(self):
        """Test that .gitignore includes Python-specific patterns."""
        # Check for __pycache__
        has_pycache = any("__pycache__" in line for line in self.gitignore_lines)
        self.assertTrue(has_pycache, ".gitignore should exclude __pycache__")
        
        # Check for *.py[cod] or individual *.pyc, *.pyo, *.pyd patterns
        has_py_compiled = any(
            "*.py[cod]" in line or "*.pyc" in line or "*.pyo" in line or "*.pyd" in line
            for line in self.gitignore_lines
        )
        self.assertTrue(
            has_py_compiled,
            ".gitignore should exclude Python compiled files (*.py[cod] or *.pyc)"
        )

    def test_gitignore_excludes_virtual_environments(self):
        """Test that .gitignore excludes virtual environment directories."""
        venv_patterns = ['venv/', 'env/', '.venv', 'ENV/', 'venv.bak/']
        found_patterns = sum(
            1 for pattern in venv_patterns 
            if any(pattern in line for line in self.gitignore_lines)
        )
        self.assertGreaterEqual(
            found_patterns,
            3,
            ".gitignore should exclude at least 3 virtual environment patterns"
        )

    def test_gitignore_excludes_build_directories(self):
        """Test that .gitignore excludes build directories."""
        build_patterns = ['build/', 'dist/', '*.egg-info/', 'eggs/']
        found_patterns = sum(
            1 for pattern in build_patterns
            if any(pattern in line for line in self.gitignore_lines)
        )
        self.assertGreaterEqual(
            found_patterns,
            2,
            ".gitignore should exclude build directories"
        )

    def test_gitignore_excludes_env_files(self):
        """Test that .gitignore excludes environment files."""
        self.assertTrue(
            any('.env' in line for line in self.gitignore_lines),
            ".gitignore should exclude .env files"
        )

    def test_gitignore_excludes_cache_directories(self):
        """Test that .gitignore excludes cache directories."""
        cache_patterns = ['.pytest_cache', '.cache', '.mypy_cache']
        found_patterns = sum(
            1 for pattern in cache_patterns
            if any(pattern in line for line in self.gitignore_lines)
        )
        self.assertGreaterEqual(
            found_patterns,
            2,
            ".gitignore should exclude cache directories"
        )

    def test_gitignore_excludes_coverage_files(self):
        """Test that .gitignore excludes coverage files."""
        coverage_patterns = ['.coverage', 'htmlcov/']
        has_coverage = any(
            any(pattern in line for pattern in coverage_patterns)
            for line in self.gitignore_lines
        )
        self.assertTrue(
            has_coverage,
            ".gitignore should exclude coverage files"
        )

    def test_gitignore_excludes_editor_files(self):
        """Test that .gitignore excludes editor-specific files."""
        editor_patterns = ['.idea/', '.vscode/', '*.swp', '.DS_Store']
        found_patterns = sum(
            1 for pattern in editor_patterns
            if any(pattern in line for line in self.gitignore_lines)
        )
        self.assertGreaterEqual(
            found_patterns,
            2,
            ".gitignore should exclude editor-specific files"
        )

    def test_gitignore_excludes_log_files(self):
        """Test that .gitignore excludes log files."""
        self.assertTrue(
            any('*.log' in line for line in self.gitignore_lines),
            ".gitignore should exclude log files"
        )

    def test_gitignore_excludes_audio_files(self):
        """Test that .gitignore excludes audio files."""
        audio_extensions = ['*.wav', '*.mp3', '*.m4a', '*.ogg', '*.flac']
        found_extensions = sum(
            1 for ext in audio_extensions
            if any(ext in line for line in self.gitignore_lines)
        )
        self.assertGreaterEqual(
            found_extensions,
            3,
            ".gitignore should exclude multiple audio file formats"
        )

    def test_gitignore_excludes_audio_directory(self):
        """Test that .gitignore excludes audio directory."""
        self.assertTrue(
            any('audio/' in line for line in self.gitignore_lines),
            ".gitignore should exclude audio/ directory"
        )

    def test_gitignore_excludes_data_files(self):
        """Test that .gitignore excludes common data files."""
        data_patterns = ['*.csv', '*.json', '*.txt']
        found_patterns = sum(
            1 for pattern in data_patterns
            if any(pattern in line for line in self.gitignore_lines)
        )
        self.assertGreaterEqual(
            found_patterns,
            2,
            ".gitignore should exclude common data file formats"
        )

    def test_gitignore_pattern_format(self):
        """Test that .gitignore patterns follow correct format."""
        for line in self.gitignore_lines:
            # Patterns shouldn't end with backslash
            self.assertFalse(
                line.endswith('\\'),
                f"Pattern '{line}' shouldn't end with backslash"
            )

    def test_gitignore_has_comments(self):
        """Test that .gitignore includes explanatory comments."""
        lines = self.gitignore_content.splitlines()
        comment_lines = [line for line in lines if line.strip().startswith('#')]
        self.assertGreater(
            len(comment_lines),
            0,
            ".gitignore should include comments for clarity"
        )

    def test_gitignore_organized_by_category(self):
        """Test that .gitignore is organized with section comments."""
        content = self.gitignore_content
        # Look for section markers (comments that categorize patterns)
        has_sections = content.count('#') >= 3
        self.assertTrue(
            has_sections,
            ".gitignore should be organized into sections with comments"
        )

    def test_gitignore_audio_directory_recent_addition(self):
        """Test that audio/ directory is included (from recent diff)."""
        has_audio_dir = any('audio/' in line for line in self.gitignore_lines)
        self.assertTrue(
            has_audio_dir,
            ".gitignore should include audio/ directory (recent addition)"
        )


class TestGitignoreConsistency(unittest.TestCase):
    """Test suite for .gitignore consistency with .dockerignore."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.project_root = Path(__file__).parent.parent
        cls.gitignore_path = cls.project_root / ".gitignore"
        cls.dockerignore_path = cls.project_root / ".dockerignore"
        
        with open(cls.gitignore_path, 'r', encoding='utf-8') as f:
            cls.gitignore_lines = set(
                line.strip() for line in f.readlines()
                if line.strip() and not line.strip().startswith('#')
            )
        
        if cls.dockerignore_path.exists():
            with open(cls.dockerignore_path, 'r', encoding='utf-8') as f:
                cls.dockerignore_lines = set(
                    line.strip() for line in f.readlines()
                    if line.strip() and not line.strip().startswith('#')
                )
        else:
            cls.dockerignore_lines = set()

    def test_common_patterns_consistency(self):
        """Test that common patterns exist in both files."""
        if not self.dockerignore_lines:
            self.skipTest(".dockerignore not found")
        
        # Patterns that should be in both files (using flexible matching)
        common_patterns = {
            "pycache": "__pycache__/",
            "pyc": "*.pyc",  # or *.py[cod] is also acceptable
            "venv": "venv/",
            "env": "env/",
            "dotenv": ".env"
        }
        
        for name, pattern in common_patterns.items():
            in_dockerignore = any(pattern in line for line in self.dockerignore_lines)
            
            if in_dockerignore:
                # For .pyc, accept either *.pyc or *.py[cod] in gitignore
                if pattern == "*.pyc":
                    in_gitignore = any(
                        "*.pyc" in line or "*.py[cod]" in line
                        for line in self.gitignore_lines
                    )
                else:
                    in_gitignore = any(pattern in line for line in self.gitignore_lines)
                
                self.assertTrue(
                    in_gitignore,
                    f"Pattern related to '{name}' in .dockerignore should also be in .gitignore"
                )

    def test_audio_directory_in_both(self):
        """Test that audio/ directory is ignored in both files."""
        if not self.dockerignore_lines:
            self.skipTest(".dockerignore not found")
        
        audio_in_gitignore = any('audio/' in line for line in self.gitignore_lines)
        audio_in_dockerignore = any('audio/' in line for line in self.dockerignore_lines)
        
        self.assertTrue(
            audio_in_gitignore,
            "audio/ should be in .gitignore"
        )
        self.assertTrue(
            audio_in_dockerignore,
            "audio/ should be in .dockerignore"
        )


if __name__ == '__main__':
    unittest.main()