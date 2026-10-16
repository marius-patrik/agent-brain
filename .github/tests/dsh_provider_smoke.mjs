import assert from 'node:assert/strict'
import { resolve } from 'node:path'
import { FileSystemSkillProvider } from '@deepseek-ai/dsh-skill-filesystem'

const root = resolve(process.argv[2])
const expected = JSON.parse(process.argv[3])
const control = new AbortController()
const provider = new FileSystemSkillProvider(
  {},
  { signal: control.signal, invalidate() {} },
  { includeDefaultRoots: false, customSkillDirs: [root], watch: false }
)
try {
  const catalog = await provider.list({ cwd: process.cwd(), signal: control.signal })
  const entries = Array.isArray(catalog) ? catalog : catalog.candidates
  assert.deepEqual(entries.map(x => x.name).sort(), expected, 'DSH filesystem provider did not discover expected skills')
  for (const entry of entries) {
    const body = await provider.get(entry, { cwd: process.cwd(), signal: control.signal })
    assert.equal(body.name, entry.name)
    assert.ok(body.content.includes('#'), `Empty DSH loaded skill: ${entry.name}`)
    assert.equal(body.resourceBase.kind, 'directory')
  }
  console.log(`DSH native provider discovered and loaded ${entries.length} Agent OS skills`)
} finally {
  control.abort()
  await provider.dispose()
}
