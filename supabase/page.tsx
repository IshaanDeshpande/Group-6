import { createClient } from '@/utils/supabase/server'
import { cookies } from 'next/headers'

type Todo = {
  id: number
  name: string
}

export default async function Page() {
  const cookieStore = await cookies()
  const supabase = createClient(cookieStore)

  let todoList: Todo[] = []
  let statusMessage = 'Loading Supabase data...'

  try {
    const { data, error } = await supabase.from('todos').select('*').limit(10)
    if (error) {
      statusMessage = `Supabase connected, but the query returned an error: ${error.message}`
    } else {
      todoList = (data ?? []) as Todo[]
      statusMessage = todoList.length > 0 ? 'Supabase data loaded successfully.' : 'Supabase connected. No todos were returned.'
    }
  } catch (error) {
    statusMessage = `Supabase connection check failed: ${error instanceof Error ? error.message : 'Unknown error'}`
  }

  return (
    <div>
      <p>{statusMessage}</p>
      <ul>
        {todoList.map((todo) => (
          <li key={todo.id}>{todo.name}</li>
        ))}
      </ul>
    </div>
  )
}