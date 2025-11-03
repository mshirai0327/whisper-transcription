"""
Comprehensive tests for Docker configuration files.
Tests the Dockerfile, .dockerignore, and their relationships.
"""

import os
import re
import unittest
from pathlib import Path


class TestDockerfile(unittest.TestCase):
    """Test suite for Dockerfile validation."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.project_root = Path(__file__).parent.parent
        cls.dockerfile_path = cls.project_root / "Dockerfile"
        
        with open(cls.dockerfile_path, 'r', encoding='utf-8') as f:
            cls.dockerfile_content = f.read()
            cls.dockerfile_lines = cls.dockerfile_content.splitlines()

    def test_dockerfile_exists(self):
        """Test that Dockerfile exists in the project root."""
        self.assertTrue(
            self.dockerfile_path.exists(),
            "Dockerfile should exist in project root"
        )

    def test_dockerfile_not_empty(self):
        """Test that Dockerfile is not empty."""
        self.assertTrue(
            len(self.dockerfile_content.strip()) > 0,
            "Dockerfile should not be empty"
        )

    def test_dockerfile_has_from_instruction(self):
        """Test that Dockerfile starts with a FROM instruction."""
        from_lines = [line for line in self.dockerfile_lines if line.strip().startswith('FROM')]
        self.assertTrue(
            len(from_lines) > 0,
            "Dockerfile should contain at least one FROM instruction"
        )
        
        # Check that FROM is one of the first non-comment, non-empty lines
        for _i, line in enumerate(self.dockerfile_lines):
            stripped = line.strip()
            if stripped and not stripped.startswith('#'):
                self.assertTrue(
                    stripped.startswith('FROM'),
                    "First non-comment instruction should be FROM"
                )
                break

    def test_dockerfile_uses_python_base_image(self):
        """Test that Dockerfile uses an official Python base image."""
        from_pattern = re.compile(r'FROM\s+python:', re.IGNORECASE)
        has_python_base = any(from_pattern.search(line) for line in self.dockerfile_lines)
        self.assertTrue(
            has_python_base,
            "Dockerfile should use an official Python base image"
        )

    def test_dockerfile_python_version(self):
        """Test that Dockerfile uses Python 3.11 as specified."""
        python_version_pattern = re.compile(r'FROM\s+python:3\.11', re.IGNORECASE)
        has_correct_version = any(
            python_version_pattern.search(line) for line in self.dockerfile_lines
        )
        self.assertTrue(
            has_correct_version,
            "Dockerfile should use Python 3.11 base image"
        )

    def test_dockerfile_uses_slim_variant(self):
        """Test that Dockerfile uses slim variant for smaller image size."""
        slim_pattern = re.compile(r'FROM\s+python:3\.11-slim', re.IGNORECASE)
        uses_slim = any(slim_pattern.search(line) for line in self.dockerfile_lines)
        self.assertTrue(
            uses_slim,
            "Dockerfile should use slim variant to reduce image size"
        )

    def test_dockerfile_sets_workdir(self):
        """Test that Dockerfile sets a WORKDIR."""
        workdir_lines = [line for line in self.dockerfile_lines if line.strip().startswith('WORKDIR')]
        self.assertTrue(
            len(workdir_lines) > 0,
            "Dockerfile should set WORKDIR"
        )

    def test_dockerfile_workdir_is_app(self):
        """Test that WORKDIR is set to /app."""
        workdir_pattern = re.compile(r'WORKDIR\s+/app', re.IGNORECASE)
        has_app_workdir = any(workdir_pattern.search(line) for line in self.dockerfile_lines)
        self.assertTrue(
            has_app_workdir,
            "Dockerfile should set WORKDIR to /app"
        )

    def test_dockerfile_sets_python_env_vars(self):
        """Test that Dockerfile sets Python environment variables."""
        content_upper = self.dockerfile_content.upper()
        self.assertIn(
            'PYTHONDONTWRITEBYTECODE',
            content_upper,
            "Dockerfile should set PYTHONDONTWRITEBYTECODE"
        )
        self.assertIn(
            'PYTHONUNBUFFERED',
            content_upper,
            "Dockerfile should set PYTHONUNBUFFERED"
        )

    def test_dockerfile_installs_ffmpeg(self):
        """Test that Dockerfile installs ffmpeg (required for whisper)."""
        content_lower = self.dockerfile_content.lower()
        self.assertIn(
            'ffmpeg',
            content_lower,
            "Dockerfile should install ffmpeg for audio processing"
        )

    def test_dockerfile_installs_build_essential(self):
        """Test that Dockerfile installs build-essential for compilation."""
        content_lower = self.dockerfile_content.lower()
        self.assertIn(
            'build-essential',
            content_lower,
            "Dockerfile should install build-essential for package compilation"
        )

    def test_dockerfile_cleans_apt_cache(self):
        """Test that Dockerfile cleans apt cache to reduce image size."""
        content_lower = self.dockerfile_content.lower()
        has_cleanup = 'rm -rf /var/lib/apt/lists' in content_lower
        self.assertTrue(
            has_cleanup,
            "Dockerfile should clean apt cache to reduce image size"
        )

    def test_dockerfile_copies_requirements(self):
        """Test that Dockerfile copies requirements.txt."""
        copy_req_pattern = re.compile(r'COPY\s+requirements\.txt', re.IGNORECASE)
        copies_requirements = any(
            copy_req_pattern.search(line) for line in self.dockerfile_lines
        )
        self.assertTrue(
            copies_requirements,
            "Dockerfile should copy requirements.txt"
        )

    def test_dockerfile_installs_requirements(self):
        """Test that Dockerfile installs Python requirements."""
        pip_install_pattern = re.compile(r'pip\s+install.*requirements\.txt', re.IGNORECASE)
        installs_requirements = any(
            pip_install_pattern.search(line) for line in self.dockerfile_lines
        )
        self.assertTrue(
            installs_requirements,
            "Dockerfile should install requirements using pip"
        )

    def test_dockerfile_uses_no_cache_dir(self):
        """Test that pip install uses --no-cache-dir flag."""
        content_lower = self.dockerfile_content.lower()
        self.assertIn(
            '--no-cache-dir',
            content_lower,
            "Dockerfile should use --no-cache-dir with pip install"
        )

    def test_dockerfile_copies_application_code(self):
        """Test that Dockerfile copies application code."""
        copy_app_pattern = re.compile(r'COPY\s+\.\s+/app/', re.IGNORECASE)
        copies_app = any(copy_app_pattern.search(line) for line in self.dockerfile_lines)
        self.assertTrue(
            copies_app,
            "Dockerfile should copy application code to /app/"
        )

    def test_dockerfile_exposes_port(self):
        """Test that Dockerfile exposes a port."""
        expose_lines = [line for line in self.dockerfile_lines if line.strip().startswith('EXPOSE')]
        self.assertTrue(
            len(expose_lines) > 0,
            "Dockerfile should expose a port"
        )

    def test_dockerfile_exposes_correct_port(self):
        """Test that Dockerfile exposes port 8010."""
        expose_pattern = re.compile(r'EXPOSE\s+8010', re.IGNORECASE)
        exposes_8010 = any(expose_pattern.search(line) for line in self.dockerfile_lines)
        self.assertTrue(
            exposes_8010,
            "Dockerfile should expose port 8010"
        )

    def test_dockerfile_has_cmd(self):
        """Test that Dockerfile has a CMD instruction."""
        cmd_lines = [line for line in self.dockerfile_lines if line.strip().startswith('CMD')]
        self.assertTrue(
            len(cmd_lines) > 0,
            "Dockerfile should have a CMD instruction"
        )

    def test_dockerfile_cmd_runs_streamlit(self):
        """Test that CMD runs streamlit."""
        cmd_lines = [line.lower() for line in self.dockerfile_lines if line.strip().lower().startswith('cmd')]
        has_streamlit = any('streamlit' in line for line in cmd_lines)
        self.assertTrue(
            has_streamlit,
            "Dockerfile CMD should run streamlit"
        )

    def test_dockerfile_cmd_runs_app_py(self):
        """Test that CMD runs app.py."""
        cmd_lines = [line.lower() for line in self.dockerfile_lines if line.strip().lower().startswith('cmd')]
        has_app_py = any('app.py' in line for line in cmd_lines)
        self.assertTrue(
            has_app_py,
            "Dockerfile CMD should run app.py"
        )

    def test_dockerfile_cmd_sets_server_port(self):
        """Test that CMD sets server.port to match EXPOSE."""
        cmd_lines = [line.lower() for line in self.dockerfile_lines if line.strip().lower().startswith('cmd')]
        has_port_config = any('--server.port' in line and '8010' in line for line in cmd_lines)
        self.assertTrue(
            has_port_config,
            "Dockerfile CMD should configure server.port to 8010"
        )

    def test_dockerfile_cmd_sets_server_address(self):
        """Test that CMD binds to 0.0.0.0 for container access."""
        cmd_lines = [line.lower() for line in self.dockerfile_lines if line.strip().lower().startswith('cmd')]
        has_address_config = any('--server.address' in line and '0.0.0.0' in line for line in cmd_lines)  # noqa: S104
        self.assertTrue(
            has_address_config,
            "Dockerfile CMD should bind to 0.0.0.0"
        )

    def test_dockerfile_cmd_sets_headless_mode(self):
        """Test that CMD runs streamlit in headless mode."""
        cmd_lines = [line.lower() for line in self.dockerfile_lines if line.strip().lower().startswith('cmd')]
        has_headless = any('--server.headless' in line and 'true' in line for line in cmd_lines)
        self.assertTrue(
            has_headless,
            "Dockerfile CMD should run streamlit in headless mode"
        )

    def test_dockerfile_layer_optimization(self):
        """Test that Dockerfile optimizes layers by combining RUN commands."""
        run_lines = [line for line in self.dockerfile_lines if line.strip().startswith('RUN')]
        # Check that apt-get update and install are in the same RUN
        apt_commands = [line for line in run_lines if 'apt-get' in line.lower()]
        if apt_commands:
            # Should have update and install in one RUN command
            combined_apt = any(
                'update' in line.lower() and 'install' in line.lower() 
                for line in apt_commands
            )
            self.assertTrue(
                combined_apt,
                "Dockerfile should combine apt-get update and install in one RUN"
            )

    def test_dockerfile_no_unnecessary_packages(self):
        """Test that apt-get install uses --no-install-recommends."""
        apt_install_lines = [
            line for line in self.dockerfile_lines 
            if 'apt-get install' in line.lower()
        ]
        if apt_install_lines:
            has_no_recommends = any(
                '--no-install-recommends' in line.lower() 
                for line in apt_install_lines
            )
            self.assertTrue(
                has_no_recommends,
                "Dockerfile should use --no-install-recommends to minimize image size"
            )

    def test_dockerfile_instruction_order(self):
        """Test that Dockerfile has instructions in optimal order for caching."""
        instruction_indices = {}
        for i, line in enumerate(self.dockerfile_lines):
            stripped = line.strip().upper()
            if stripped.startswith('FROM'):
                instruction_indices['FROM'] = i
            elif stripped.startswith('WORKDIR'):
                instruction_indices.setdefault('WORKDIR', i)
            elif 'requirements.txt' in line and 'COPY' in stripped:
                instruction_indices.setdefault('COPY_REQ', i)
            elif 'pip install' in line.lower():
                instruction_indices.setdefault('PIP_INSTALL', i)
            elif stripped.startswith('COPY . '):
                instruction_indices.setdefault('COPY_APP', i)
        
        # Requirements should be copied and installed before app code
        if 'COPY_REQ' in instruction_indices and 'COPY_APP' in instruction_indices:
            self.assertLess(
                instruction_indices['COPY_REQ'],
                instruction_indices['COPY_APP'],
                "requirements.txt should be copied before application code for better caching"
            )
        
        if 'PIP_INSTALL' in instruction_indices and 'COPY_APP' in instruction_indices:
            self.assertLess(
                instruction_indices['PIP_INSTALL'],
                instruction_indices['COPY_APP'],
                "Dependencies should be installed before copying application code"
            )


class TestDockerignore(unittest.TestCase):
    """Test suite for .dockerignore file validation."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.project_root = Path(__file__).parent.parent
        cls.dockerignore_path = cls.project_root / ".dockerignore"
        
        with open(cls.dockerignore_path, 'r', encoding='utf-8') as f:
            cls.dockerignore_content = f.read()
            cls.dockerignore_lines = [
                line.strip() for line in cls.dockerignore_content.splitlines()
                if line.strip() and not line.strip().startswith('#')
            ]

    def test_dockerignore_exists(self):
        """Test that .dockerignore exists."""
        self.assertTrue(
            self.dockerignore_path.exists(),
            ".dockerignore should exist in project root"
        )

    def test_dockerignore_not_empty(self):
        """Test that .dockerignore is not empty."""
        self.assertTrue(
            len(self.dockerignore_lines) > 0,
            ".dockerignore should not be empty"
        )

    def test_dockerignore_excludes_pycache(self):
        """Test that .dockerignore excludes __pycache__."""
        has_pycache = any('__pycache__' in line for line in self.dockerignore_lines)
        self.assertTrue(
            has_pycache,
            ".dockerignore should exclude __pycache__ directories"
        )

    def test_dockerignore_excludes_pyc_files(self):
        """Test that .dockerignore excludes .pyc files."""
        has_pyc = any('.pyc' in line for line in self.dockerignore_lines)
        self.assertTrue(
            has_pyc,
            ".dockerignore should exclude .pyc files"
        )

    def test_dockerignore_excludes_virtual_environments(self):
        """Test that .dockerignore excludes virtual environments."""
        venv_patterns = ['venv/', 'env/', '.venv', 'ENV/']
        has_venv = any(
            any(pattern in line for pattern in venv_patterns)
            for line in self.dockerignore_lines
        )
        self.assertTrue(
            has_venv,
            ".dockerignore should exclude virtual environment directories"
        )

    def test_dockerignore_excludes_git(self):
        """Test that .dockerignore excludes .git directory."""
        has_git = any('.git' in line for line in self.dockerignore_lines)
        self.assertTrue(
            has_git,
            ".dockerignore should exclude .git directory"
        )

    def test_dockerignore_excludes_env_files(self):
        """Test that .dockerignore excludes .env files."""
        has_env = any('.env' in line for line in self.dockerignore_lines)
        self.assertTrue(
            has_env,
            ".dockerignore should exclude .env files"
        )

    def test_dockerignore_excludes_audio_files(self):
        """Test that .dockerignore excludes audio files."""
        audio_extensions = ['.wav', '.mp3', '.ogg', '.flac']
        has_audio = any(
            any(ext in line for ext in audio_extensions)
            for line in self.dockerignore_lines
        )
        self.assertTrue(
            has_audio,
            ".dockerignore should exclude audio files"
        )

    def test_dockerignore_excludes_audio_directory(self):
        """Test that .dockerignore excludes audio directory."""
        has_audio_dir = any('audio/' in line for line in self.dockerignore_lines)
        self.assertTrue(
            has_audio_dir,
            ".dockerignore should exclude audio/ directory"
        )

    def test_dockerignore_excludes_test_cache(self):
        """Test that .dockerignore excludes test cache directories."""
        cache_patterns = ['.pytest_cache', '.mypy_cache']
        has_cache = any(
            any(pattern in line for pattern in cache_patterns)
            for line in self.dockerignore_lines
        )
        self.assertTrue(
            has_cache,
            ".dockerignore should exclude test cache directories"
        )

    def test_dockerignore_excludes_build_artifacts(self):
        """Test that .dockerignore excludes build artifacts."""
        build_patterns = ['dist/', 'build/', '*.egg-info']
        has_build = any(
            any(pattern in line for pattern in build_patterns)
            for line in self.dockerignore_lines
        )
        self.assertTrue(
            has_build,
            ".dockerignore should exclude build artifacts"
        )

    def test_dockerignore_excludes_database_files(self):
        """Test that .dockerignore excludes database files."""
        has_db = any('.sqlite3' in line or '*.db' in line for line in self.dockerignore_lines)
        self.assertTrue(
            has_db,
            ".dockerignore should exclude database files"
        )

    def test_dockerignore_pattern_validity(self):
        """Test that .dockerignore patterns are valid."""
        for line in self.dockerignore_lines:
            # Basic validation: patterns shouldn't have obvious syntax errors
            self.assertFalse(
                line.endswith('\\'),
                f"Pattern '{line}' shouldn't end with backslash"
            )
            # Check for common mistakes
            self.assertNotIn(
                ' ',
                line.strip(),
                f"Pattern '{line}' shouldn't contain spaces"
            )


class TestDockerIntegration(unittest.TestCase):
    """Test suite for Docker configuration integration."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.project_root = Path(__file__).parent.parent
        cls.dockerfile_path = cls.project_root / "Dockerfile"
        cls.dockerignore_path = cls.project_root / ".dockerignore"
        cls.requirements_path = cls.project_root / "requirements.txt"
        cls.app_path = cls.project_root / "app.py"

    def test_required_files_exist(self):
        """Test that all required files for Docker build exist."""
        required_files = [
            self.dockerfile_path,
            self.dockerignore_path,
            self.requirements_path,
            self.app_path
        ]
        for file_path in required_files:
            self.assertTrue(
                file_path.exists(),
                f"Required file {file_path.name} should exist"
            )

    def test_dockerfile_references_existing_files(self):
        """Test that Dockerfile only references files that exist."""
        with open(self.dockerfile_path, 'r', encoding='utf-8') as f:
            dockerfile_content = f.read()
        
        # Check requirements.txt is referenced and exists
        if 'requirements.txt' in dockerfile_content:
            self.assertTrue(
                self.requirements_path.exists(),
                "requirements.txt referenced in Dockerfile should exist"
            )
        
        # Check app.py is referenced and exists
        if 'app.py' in dockerfile_content:
            self.assertTrue(
                self.app_path.exists(),
                "app.py referenced in Dockerfile should exist"
            )

    def test_port_consistency(self):
        """Test that port in CMD matches EXPOSE directive."""
        with open(self.dockerfile_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        exposed_ports = []
        cmd_ports = []
        
        for line in lines:
            if line.strip().startswith('EXPOSE'):
                port_match = re.search(r'EXPOSE\s+(\d+)', line)
                if port_match:
                    exposed_ports.append(port_match.group(1))
            elif line.strip().startswith('CMD'):
                port_match = re.search(r'--server\.port["\s]+(\d+)', line)
                if port_match:
                    cmd_ports.append(port_match.group(1))
        
        if exposed_ports and cmd_ports:
            self.assertEqual(
                exposed_ports[0],
                cmd_ports[0],
                "EXPOSE port should match --server.port in CMD"
            )

    def test_requirements_has_streamlit(self):
        """Test that requirements.txt includes streamlit (needed for CMD)."""
        with open(self.requirements_path, 'r', encoding='utf-8') as f:
            requirements = f.read().lower()
        
        self.assertIn(
            'streamlit',
            requirements,
            "requirements.txt should include streamlit"
        )

    def test_requirements_has_whisper(self):
        """Test that requirements.txt includes whisper."""
        with open(self.requirements_path, 'r', encoding='utf-8') as f:
            requirements = f.read().lower()
        
        has_whisper = 'whisper' in requirements or 'openai-whisper' in requirements
        self.assertTrue(
            has_whisper,
            "requirements.txt should include whisper"
        )


if __name__ == '__main__':
    unittest.main()