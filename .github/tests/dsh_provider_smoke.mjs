import assert from 'node:assert/strict'
import { resolve } from 'node:path'
import { Context } from '@deepseek-ai/cordis'
import SkillRegistry from '@deepseek-ai/dsh-skill'
import * as SkillFileSystem from '@deepseek-ai/dsh-skill-filesystem'

const root = resolve(process.argv[2])
const expected = JSON.parse(process.argv[3])
const ctx = new Context()

await ctx.plugin(SkillRegistry)
await ctx.plugin(SkillFileSystem, {
  includeDefaultRoots: false,
  customSkillDirs: [root],
  watch: false,
})
try {
  const catalog = await ctx.skills.list({ cwd: process.cwd() })
  assert.deepEqual(catalog.map(x => x.name).sort(), expected, 'DSH did not discover the bundled skills')
  for (const entry of catalog) {
    const body = await ctx.skills.get(entry.name)
    assert.ok(body, `DSH could not load skill: ${entry.name}`)
    assert.equal(body.name, entry.name)
    assert.ok(body.content.includes('#'), `Empty DSH loaded skill: ${entry.name}`)
    assert.equal(body.resourceBase.kind, 'directory')
  }
  console.log(`DSH native registry discovered and loaded ${catalog.length} Agent OS skills`)
} finally {
  await ctx.fiber.dispose()
}
