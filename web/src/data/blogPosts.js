import posts from './blogPosts.json'

export const blogPosts = posts

export function getBlogPost(slug) {
  return blogPosts.find((post) => post.slug === slug) || null
}

export function getFeaturedPosts() {
  return blogPosts.filter((post) => post.featured)
}

export function formatBlogDate(dateStr) {
  if (!dateStr) return ''
  const [y, m, d] = dateStr.split('-')
  return `${y}年${Number(m)}月${Number(d)}日`
}
