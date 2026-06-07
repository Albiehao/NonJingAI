import request from './request'

export function chat(message, userId) {
  return request({
    url: '/chat',
    method: 'post',
    data: {
      message,
      userId
    }
  })
}

export function chatStream(message, { onToken, onRecommendations, onComplete, onError }) {
  return new Promise((resolve, reject) => {
    const url = 'http://localhost:8080/chat/stream'
    let completed = false

    const completeOnce = () => {
      if (completed) return
      completed = true
      onComplete && onComplete()
      resolve()
    }

    const failOnce = (errorMessage) => {
      if (completed) return
      completed = true
      const msg = errorMessage || 'Stream error'
      onError && onError(msg)
      reject(new Error(msg))
    }

    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': localStorage.getItem('token') ? 'Bearer ' + localStorage.getItem('token') : ''
      },
      body: JSON.stringify({ message })
    })
      .then(response => {
        if (!response.ok) {
          failOnce(`HTTP ${response.status}`)
          return
        }
        if (!response.body) {
          failOnce('SSE response body is empty')
          return
        }

        const reader = response.body.getReader()
        const decoder = new TextDecoder()
        let buffer = ''

        const processBuffer = () => {
          buffer = buffer.replace(/\r\n/g, '\n')

          while (buffer.includes('\n\n')) {
            const eventEnd = buffer.indexOf('\n\n')
            const eventBlock = buffer.substring(0, eventEnd)
            buffer = buffer.substring(eventEnd + 2)

            const lines = eventBlock.split('\n')
            let eventType = ''
            let eventData = ''

            for (const line of lines) {
              if (line.startsWith('event:')) {
                eventType = line.substring(6).trim()
              } else if (line.startsWith('data:')) {
                eventData += line.substring(5).trim()
              }
            }

            if (!eventType) {
              continue
            }

            switch (eventType) {
              case 'token':
                onToken && onToken(eventData)
                break
              case 'recommendations':
                if (!eventData) break
                try {
                  const recommendations = JSON.parse(eventData)
                  onRecommendations && onRecommendations(recommendations)
                } catch (parseError) {
                  console.error('Failed to parse recommendations:', parseError, eventData)
                }
                break
              case 'done':
                completeOnce()
                return
              case 'error':
                failOnce(eventData || 'Stream error')
                return
              default:
                break
            }
          }
        }

        const readChunk = () => {
          reader.read()
            .then(({ done, value }) => {
              if (done) {
                if (buffer.trim()) {
                  processBuffer()
                }
                // Safety net: close even if backend didn't emit done event.
                completeOnce()
                return
              }

              buffer += decoder.decode(value, { stream: true })
              processBuffer()
              readChunk()
            })
            .catch(err => {
              failOnce(err.message || 'Read stream failed')
            })
        }

        readChunk()
      })
      .catch(err => {
        failOnce(err.message || 'Request failed')
      })
  })
}
