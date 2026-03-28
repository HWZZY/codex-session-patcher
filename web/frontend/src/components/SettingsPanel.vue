<template>
  <div class="settings-panel">
    <n-space vertical size="large">
      <!-- AI 配置 -->
      <n-card title="AI 配置" size="small">
        <template #header-extra>
          <n-tag :type="settingsStore.aiEnabled ? 'success' : 'default'" size="small">
            {{ settingsStore.aiEnabled ? '已启用' : '未启用' }}
          </n-tag>
        </template>

        <n-space vertical>
          <n-form-item label="启用 AI">
            <n-switch
              v-model:value="settingsStore.aiEnabled"
              @update:value="settingsStore.markChanged"
            />
          </n-form-item>

          <n-collapse-transition :show="settingsStore.aiEnabled">
            <n-form-item label="API Endpoint">
              <n-input
                v-model:value="settingsStore.aiEndpoint"
                placeholder="https://api.openai.com/v1"
                @update:value="settingsStore.markChanged"
              />
              <template #feedback>
                <span class="form-hint">支持 OpenAI 兼容接口（OpenAI / Ollama / OpenRouter 等）</span>
              </template>
            </n-form-item>

            <n-form-item label="API Key">
              <n-input
                v-model:value="settingsStore.aiKey"
                type="password"
                show-password-on="click"
                placeholder="sk-..."
                @update:value="settingsStore.markChanged"
              />
              <template #feedback>
                <span class="form-hint">本地模型（如 Ollama）可留空</span>
              </template>
            </n-form-item>

            <n-form-item label="模型名称">
              <n-input
                v-model:value="settingsStore.aiModel"
                placeholder="gpt-4o / deepseek-chat / ..."
                @update:value="settingsStore.markChanged"
              />
            </n-form-item>
          </n-collapse-transition>

          <n-alert type="info" :bordered="false">
            AI 用于「提示词改写」和「会话清理」时的智能回复生成
          </n-alert>
        </n-space>
      </n-card>

      <!-- 会话清理配置 -->
      <n-card title="会话清理" size="small">
        <n-space vertical>
          <n-form-item label="启用 Claude Code 支持">
            <n-switch
              :value="settingsStore.claudeCodeEnabled"
              @update:value="settingsStore.setClaudeCodeEnabled"
            />
            <template #feedback>
              <span class="form-hint">开启后可管理 Claude Code 会话、使用 Claude Code CTF 模式</span>
            </template>
          </n-form-item>

          <n-form-item label="显示全部会话">
            <n-switch
              :value="settingsStore.showAllSessions"
              @update:value="settingsStore.setShowAllSessions"
            />
            <template #feedback>
              <span class="form-hint">关闭时仅显示有拒绝和已清理的会话，减少列表干扰</span>
            </template>
          </n-form-item>

          <n-form-item label="默认替换文本">
            <n-input
              v-model:value="settingsStore.mockResponse"
              type="textarea"
              :rows="3"
              placeholder="检测到拒绝回复时，替换为此文本"
              @update:value="settingsStore.markChanged"
            />
            <template #feedback>
              <span class="form-hint">未启用 AI 时使用此固定文本替换拒绝内容</span>
            </template>
          </n-form-item>
        </n-space>
      </n-card>

      <!-- 拒绝检测 -->
      <n-card title="拒绝检测关键词" size="small">
        <n-space vertical>
          <n-form-item label="内置中文关键词">
            <div class="builtin-keywords">
              <n-tag v-for="kw in builtinZhKeywords" :key="kw" size="small" type="info" :bordered="false">{{ kw }}</n-tag>
            </div>
          </n-form-item>

          <n-form-item label="内置英文关键词">
            <div class="builtin-keywords">
              <n-tag v-for="kw in builtinEnKeywords" :key="kw" size="small" type="info" :bordered="false">{{ kw }}</n-tag>
            </div>
          </n-form-item>

          <n-form-item label="自定义中文关键词">
            <n-dynamic-tags
              :value="zhKeywords"
              @update:value="handleKeywordsChange('zh', $event)"
            />
          </n-form-item>

          <n-form-item label="自定义英文关键词">
            <n-dynamic-tags
              :value="enKeywords"
              @update:value="handleKeywordsChange('en', $event)"
            />
          </n-form-item>
        </n-space>
      </n-card>

      <!-- 保存按钮 -->
      <n-space justify="end">
        <n-button @click="handleReset">重置</n-button>
        <n-button
          type="primary"
          :disabled="!settingsStore.changed"
          :loading="settingsStore.loading"
          @click="handleSave"
        >
          保存
        </n-button>
      </n-space>
    </n-space>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useMessage } from 'naive-ui'
import { useSettingsStore } from '../stores/settingsStore'

const message = useMessage()
const settingsStore = useSettingsStore()

// 内置关键词
const builtinZhKeywords = [
  '抱歉', '无法', '违反', '不能', '拒绝', '不允许', '禁止',
  '很抱歉', '对不起', '不好意思', '我无法', '我不能'
]
const builtinEnKeywords = [
  'sorry', 'cannot', 'apologize', 'violate', 'policy',
  'as an AI', 'I cannot', "I'm unable", 'not able to',
  'against my', "I won't", 'refuse to', 'unable to',
  'I apologize', 'not permitted', 'not allowed'
]

// 自定义关键词
const zhKeywords = computed(() => settingsStore.customKeywords.zh || [])
const enKeywords = computed(() => settingsStore.customKeywords.en || [])

function handleKeywordsChange(lang, value) {
  settingsStore.customKeywords[lang] = value
  settingsStore.markChanged()
}

async function handleSave() {
  try {
    await settingsStore.saveSettings()
    message.success('设置已保存')
  } catch (error) {
    message.error('保存失败: ' + error.message)
  }
}

function handleReset() {
  settingsStore.resetSettings()
  message.info('已重置为默认值')
}
</script>

<style scoped>
.settings-panel {
  max-width: 800px;
  margin: 0 auto;
}

.n-card {
  background: var(--color-bg-1);
}

.form-hint {
  font-size: 11px;
  color: #666;
}

.builtin-keywords {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}
</style>