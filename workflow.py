"""Lesson-specific workflow. Read this file before the execution adapter."""
from __future__ import annotations
import asyncio
import json
from pathlib import Path
from runtime import atomic_json, contained_path, in_process_tool

async def run(agent, data):
    owner = data['owner']
    if not owner.isalnum():
        raise ValueError('Owner must be alphanumeric')
    path = agent.root / 'state' / f'{owner}.json'
    record = {'owner': owner, 'role': data['role'], 'source': 'explicit user input'}
    atomic_json(path, record)
    memory = json.loads(path.read_text(encoding='utf8'))
    answer = await agent.ask('personalize', 'Suggest two ideas using only the stated role. Do not infer an employer or budget.',
        {'request': data['request'], 'memory': memory}, 'Try a customer interview series and a small newsletter experiment.')
    return {'memory_supplied': memory, 'answer': answer, 'forget': f'Delete {path.name} from state to forget this record.'}
