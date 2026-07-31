import { ref, computed } from 'vue'

/**
 * @typedef {Object} MentionKnowledgeBase
 * @property {string} db_id - 知识库ID
 * @property {string} name - 知识库名称
 */

/**
 * @typedef {Object} MentionConfig
 * @property {MentionFile[]} [files] - 可引用的文件列表
 * @property {MentionKnowledgeBase[]} [knowledgeBases] - 可引用的知识库列表
 */

/**
 * @typedef {Object} MentionItem
 * @property {string} value - 显示和插入的值
 * @property {string} label - 显示标签
 * @property {'file'|'knowledge'} type - 类型
 * @property {string} [description] - 描述信息
 */

/**
 * @typedef {Object} UseMentionReturn
 * @property {import('vue').Ref<MentionConfig>} mentionConfig - 当前的 mention 配置
 * @property {Function} setMention - 设置 mention 配置
 * @property {Function} updateFiles - 更新文件列表
 * @property {Function} updateKnowledgeBases - 更新知识库列表
 * @property {Function} getFilteredItems - 根据查询获取过滤后的候选列表
 */

/**
 * Mention @提及 功能管理
 * @returns {UseMentionReturn}
 */
export function useMention() {
  const mentionConfig = ref({
    files: [],
    knowledgeBases: [],
  })

  /**
   * 设置完整的 mention 配置
   * @param {MentionConfig} config
   */
  const setMention = (config) => {
    mentionConfig.value = {
      files: config.files || [],
      knowledgeBases: config.knowledgeBases || [],
    }
  }

  /**
   * 更新文件列表
   * @param {MentionFile[]} files
   */
  const updateFiles = (files) => {
    mentionConfig.value.files = files || []
  }

  /**
   * 更新知识库列表
   * @param {MentionKnowledgeBase[]} knowledgeBases
   */
  const updateKnowledgeBases = (knowledgeBases) => {
    mentionConfig.value.knowledgeBases = knowledgeBases || []
  }

  /**
   * 获取分类后的所有候选项
   * @returns {{ files: MentionItem[], knowledgeBases: MentionItem[] }}
   */
  const getCategorizedItems = () => {
    const { files, knowledgeBases } = mentionConfig.value

    const fileItems = files.map((f) => ({
      value: f.path,
      label: f.path.split('/').pop() || f.path,
      type: 'file',
      description: f.path
    }))

    const kbItems = knowledgeBases.map((kb) => ({
      value: kb.name,
      label: kb.name,
      type: 'knowledge',
      description: kb.db_id
    }))

    return {
      files: fileItems,
      knowledgeBases: kbItems,
    }
  }

  /**
   * 根据查询字符串过滤候选项
   * @param {string} query - 查询字符串（不含 @ 符号）
   * @returns {{ files: MentionItem[], knowledgeBases: MentionItem[] }}
   */
  const getFilteredItems = (query = '') => {
    const lowerQuery = query.toLowerCase()
    const categorized = getCategorizedItems()

    const filterItems = (items) =>
      items.filter(
        (item) =>
          item.label.toLowerCase().includes(lowerQuery) ||
          item.value.toLowerCase().includes(lowerQuery)
      )

    return {
      files: filterItems(categorized.files),
      knowledgeBases: filterItems(categorized.knowledgeBases),
    }
  }

  return {
    mentionConfig,
    setMention,
    updateFiles,
    updateKnowledgeBases,
    getFilteredItems,
    getCategorizedItems
  }
}
