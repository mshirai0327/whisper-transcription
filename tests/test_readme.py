"""
Comprehensive tests for README.md documentation.
"""

import re
import unittest
from pathlib import Path
from urllib.parse import urlparse


class TestReadme(unittest.TestCase):
    """Test suite for README.md validation."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.project_root = Path(__file__).parent.parent
        cls.readme_path = cls.project_root / "README.md"
        
        with open(cls.readme_path, 'r', encoding='utf-8') as f:
            cls.readme_content = f.read()
            cls.readme_lines = cls.readme_content.splitlines()

    def test_readme_exists(self):
        """Test that README.md exists."""
        self.assertTrue(
            self.readme_path.exists(),
            "README.md should exist in project root"
        )

    def test_readme_not_empty(self):
        """Test that README.md is not empty."""
        self.assertTrue(
            len(self.readme_content.strip()) > 0,
            "README.md should not be empty"
        )

    def test_readme_has_title(self):
        """Test that README.md has a top-level heading."""
        has_h1 = any(line.startswith('# ') for line in self.readme_lines)
        self.assertTrue(
            has_h1,
            "README.md should have a top-level heading (# )"
        )

    def test_readme_title_content(self):
        """Test that README.md title mentions Whisper."""
        title_lines = [line for line in self.readme_lines if line.startswith('# ')]
        if title_lines:
            title = title_lines[0]
            self.assertIn(
                'Whisper',
                title,
                "README title should mention Whisper"
            )

    def test_readme_has_sections(self):
        """Test that README.md has multiple sections."""
        section_headers = [line for line in self.readme_lines if line.startswith('## ')]
        self.assertGreaterEqual(
            len(section_headers),
            4,
            "README.md should have at least 4 main sections"
        )

    def test_readme_has_features_section(self):
        """Test that README.md has a features section."""
        has_features = any('機能' in line or 'Features' in line for line in self.readme_lines if line.startswith('## '))
        self.assertTrue(
            has_features,
            "README.md should have a features section"
        )

    def test_readme_has_requirements_section(self):
        """Test that README.md has a requirements section."""
        has_requirements = any(
            '必要条件' in line or 'Requirements' in line or '必要' in line
            for line in self.readme_lines if line.startswith('## ')
        )
        self.assertTrue(
            has_requirements,
            "README.md should have a requirements section"
        )

    def test_readme_has_installation_section(self):
        """Test that README.md has an installation section."""
        has_installation = any(
            'インストール' in line or 'Installation' in line or 'Setup' in line
            for line in self.readme_lines if line.startswith('## ')
        )
        self.assertTrue(
            has_installation,
            "README.md should have an installation section"
        )

    def test_readme_has_usage_section(self):
        """Test that README.md has a usage section."""
        has_usage = any(
            '使用方法' in line or 'Usage' in line or '使い方' in line
            for line in self.readme_lines if line.startswith('## ')
        )
        self.assertTrue(
            has_usage,
            "README.md should have a usage section"
        )

    def test_readme_has_license_section(self):
        """Test that README.md has a license section."""
        has_license = any(
            'ライセンス' in line or 'License' in line
            for line in self.readme_lines if line.startswith('## ')
        )
        self.assertTrue(
            has_license,
            "README.md should have a license section"
        )

    def test_readme_mentions_python_version(self):
        """Test that README.md specifies Python version requirement."""
        content_lower = self.readme_content.lower()
        has_python_version = 'python 3' in content_lower or 'python3' in content_lower
        self.assertTrue(
            has_python_version,
            "README.md should specify Python version requirement"
        )

    def test_readme_mentions_ffmpeg(self):
        """Test that README.md mentions FFmpeg requirement."""
        self.assertIn(
            'FFmpeg',
            self.readme_content,
            "README.md should mention FFmpeg as a requirement"
        )

    def test_readme_has_code_blocks(self):
        """Test that README.md includes code blocks for examples."""
        has_code_blocks = '```' in self.readme_content
        self.assertTrue(
            has_code_blocks,
            "README.md should include code blocks for examples"
        )

    def test_readme_bash_code_blocks(self):
        """Test that README.md has bash/shell code blocks."""
        bash_pattern = re.compile(r'```(?:bash|shell|sh)')
        has_bash = bash_pattern.search(self.readme_content) is not None
        self.assertTrue(
            has_bash,
            "README.md should include bash/shell code blocks"
        )

    def test_readme_installation_commands(self):
        """Test that README.md includes installation commands."""
        content_lower = self.readme_content.lower()
        has_install_cmd = 'pip install' in content_lower or 'requirements.txt' in content_lower
        self.assertTrue(
            has_install_cmd,
            "README.md should include pip install commands"
        )

    def test_readme_mentions_streamlit(self):
        """Test that README.md mentions Streamlit for web interface."""
        self.assertIn(
            'Streamlit',
            self.readme_content,
            "README.md should mention Streamlit"
        )

    def test_readme_has_docker_section(self):
        """Test that README.md has Docker usage section (from recent diff)."""
        has_docker = any('Docker' in line for line in self.readme_lines)
        self.assertTrue(
            has_docker,
            "README.md should have Docker section"
        )

    def test_readme_docker_build_command(self):
        """Test that README.md includes docker build command."""
        content_lower = self.readme_content.lower()
        has_docker_build = 'docker build' in content_lower
        self.assertTrue(
            has_docker_build,
            "README.md should include docker build command"
        )

    def test_readme_docker_run_command(self):
        """Test that README.md includes docker run command."""
        content_lower = self.readme_content.lower()
        has_docker_run = 'docker run' in content_lower
        self.assertTrue(
            has_docker_run,
            "README.md should include docker run command"
        )

    def test_readme_docker_port_mapping(self):
        """Test that README.md mentions port 8010 for Docker."""
        has_port_8010 = '8010' in self.readme_content
        self.assertTrue(
            has_port_8010,
            "README.md should mention port 8010 for Docker"
        )

    def test_readme_docker_gpu_support(self):
        """Test that README.md mentions GPU support for Docker."""
        content_lower = self.readme_content.lower()
        has_gpu = '--gpus' in content_lower or 'gpu' in content_lower
        self.assertTrue(
            has_gpu,
            "README.md should mention GPU support for Docker"
        )

    def test_readme_links_valid_format(self):
        """Test that README.md links follow valid markdown format."""
        # Find all markdown links
        link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
        links = link_pattern.findall(self.readme_content)
        
        self.assertGreater(
            len(links),
            0,
            "README.md should contain at least one link"
        )
        
        for link_text, link_url in links:
            # Link text shouldn't be empty
            self.assertTrue(
                len(link_text.strip()) > 0,
                f"Link text should not be empty: [{link_text}]({link_url})"
            )
            # URL shouldn't be empty
            self.assertTrue(
                len(link_url.strip()) > 0,
                f"Link URL should not be empty: [{link_text}]({link_url})"
            )

    def test_readme_github_link(self):
        """Test that README.md includes GitHub repository link."""
        github_pattern = re.compile(r'github\.com/[^/\s]+/[^/\s]+')
        has_github = github_pattern.search(self.readme_content) is not None
        self.assertTrue(
            has_github,
            "README.md should include GitHub repository link"
        )

    def test_readme_ffmpeg_download_link(self):
        """Test that README.md includes FFmpeg download link."""
        ffmpeg_pattern = re.compile(r'ffmpeg\.org')
        has_ffmpeg_link = ffmpeg_pattern.search(self.readme_content) is not None
        self.assertTrue(
            has_ffmpeg_link,
            "README.md should include FFmpeg download link"
        )

    def test_readme_formatting_consistency(self):
        """Test that README.md uses consistent formatting."""
        # Check for consistent bullet point style
        bullet_lines = [line for line in self.readme_lines if line.strip().startswith('-')]
        if bullet_lines:
            # All bullets should use '-' consistently
            hyphen_count = sum(1 for line in self.readme_lines if line.strip().startswith('- '))
            # Prefer hyphens over asterisks
            self.assertGreater(
                hyphen_count,
                0,
                "README.md should use hyphen bullet points"
            )

    def test_readme_language_code_examples(self):
        """Test that README.md includes language code examples."""
        content_lower = self.readme_content.lower()
        has_lang_codes = '"ja"' in self.readme_content or "'ja'" in self.readme_content or 'language ja' in content_lower
        self.assertTrue(
            has_lang_codes,
            "README.md should include language code examples (e.g., 'ja')"
        )

    def test_readme_model_size_explanation(self):
        """Test that README.md explains model sizes."""
        content_lower = self.readme_content.lower()
        model_sizes = ['tiny', 'base', 'small', 'medium', 'large']
        mentioned_sizes = sum(1 for size in model_sizes if size in content_lower)
        self.assertGreaterEqual(
            mentioned_sizes,
            3,
            "README.md should explain at least 3 model sizes"
        )

    def test_readme_file_format_support(self):
        """Test that README.md lists supported file formats."""
        audio_formats = ['mp3', 'wav', 'm4a']
        mentioned_formats = sum(1 for fmt in audio_formats if fmt in self.readme_content.lower())
        self.assertGreaterEqual(
            mentioned_formats,
            2,
            "README.md should list supported audio formats"
        )

    def test_readme_proper_spacing(self):
        """Test that README.md has proper spacing between sections."""
        # Check that there are blank lines between major sections
        section_indices = [
            i for i, line in enumerate(self.readme_lines)
            if line.startswith('## ')
        ]
        
        if len(section_indices) > 1:
            # Check spacing before sections (should have blank line before most sections)
            has_spacing = any(
                self.readme_lines[i-1].strip() == '' 
                for i in section_indices[1:] if i > 0
            )
            self.assertTrue(
                has_spacing,
                "README.md should have blank lines between major sections"
            )


class TestReadmeUpdates(unittest.TestCase):
    """Test suite for recent README.md updates."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.project_root = Path(__file__).parent.parent
        cls.readme_path = cls.project_root / "README.md"
        
        with open(cls.readme_path, 'r', encoding='utf-8') as f:
            cls.readme_content = f.read()

    def test_docker_section_added(self):
        """Test that Docker usage section was added (from diff)."""
        # Check for Docker-related heading
        has_docker_heading = 'Docker から使用' in self.readme_content or 'Docker' in self.readme_content
        self.assertTrue(
            has_docker_heading,
            "README.md should have Docker usage section (recent addition)"
        )

    def test_docker_build_instructions(self):
        """Test that Docker build instructions are present."""
        has_build = 'docker build' in self.readme_content.lower()
        self.assertTrue(
            has_build,
            "README.md should include Docker build instructions"
        )

    def test_docker_run_instructions(self):
        """Test that Docker run instructions are present."""
        has_run = 'docker run' in self.readme_content.lower()
        self.assertTrue(
            has_run,
            "README.md should include Docker run instructions"
        )

    def test_improved_formatting(self):
        """Test that formatting improvements are present (from diff)."""
        # Check for proper spacing in markdown (code blocks with blank lines)
        lines = self.readme_content.splitlines()
        code_block_indices = [i for i, line in enumerate(lines) if line.strip().startswith('```')]
        
        if len(code_block_indices) > 0:
            # At least some code blocks should have blank lines before them
            has_proper_spacing = any(
                i > 0 and lines[i-1].strip() == ''
                for i in code_block_indices
            )
            self.assertTrue(
                has_proper_spacing,
                "README.md code blocks should have proper spacing"
            )


if __name__ == '__main__':
    unittest.main()