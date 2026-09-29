"""Frozen D/E Claude isolation wrapper, subscription authentication only."""
import json
import os

MODEL = 'claude-fable-5-1[1m]'


def command(cfg, schema, session):
    if cfg['requested_model'] != MODEL:
        raise ValueError('Fable model fallback rejected')
    settings = {'disableAllHooks': True, 'autoMemoryEnabled': False,
                'enabledPlugins': {'agents-md@builtin': False, 'telemetry@builtin': False},
                'disableClaudeAiConnectors': True, 'syncClaudeAiSkills': False,
                'syncClaudeAiPlugins': False}
    return [cfg['cli'], '--print', '--safe-mode', '--setting-sources', '',
            '--settings', json.dumps(settings), '--strict-mcp-config',
            '--mcp-config', '{"mcpServers":{}}', '--tools', '',
            '--disable-slash-commands', '--no-session-persistence', '--session-id', session,
            '--model', MODEL, '--effort', cfg['reasoning_effort'],
            '--output-format', 'stream-json', '--verbose', '--json-schema', schema]


def environment():
    return {k: v for k, v in os.environ.items()
            if not k.startswith(('CODEX_', 'CLAUDE_', 'ANTHROPIC_', 'OPENAI_', 'META_'))
            and k != 'CLAUDECODE'}
