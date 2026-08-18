import streamlit as st
import pickle

# Título de la aplicación
st.title("Lista de Tareas (To-Do List)")

# Cargar la lista de tareas desde un archivo si existe
try:
    with open('tasks.pkl', 'rb') as f:
        tasks = pickle.load(f)
except FileNotFoundError:
    tasks = []

# Función para agregar una tarea
def add_task(text, priority):
    tasks.append({'text': text, 'priority': priority, 'completed': False})
    with open('tasks.pkl', 'wb') as f:
        pickle.dump(tasks, f)

# Función para marcar una tarea como completada
def mark_task(index):
    tasks[index]['completed'] = True
    with open('tasks.pkl', 'wb') as f:
        pickle.dump(tasks, f)

# Función para eliminar una tarea
def delete_task(index):
    del tasks[index]
    with open('tasks.pkl', 'wb') as f:
        pickle.dump(tasks, f)

# Formulario para agregar una nueva tarea
with st.form(key='task_form'):
    task_text = st.text_input('Nueva tarea:')
    priority = st.selectbox('Prioridad', ['Alta', 'Media', 'Baja'])
    if st.form_submit_button('Agregar Tarea'):
        add_task(task_text, priority)

# Mostrar las tareas en la pantalla
if tasks:
    st.write('### Tareas Pendientes:')
    for i, task in enumerate(tasks):
        if not task['completed']:
            with st.container():
                st.write(f"{i + 1}. **{task['text']}** - {task['priority']}")
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    if st.button('Marcar como Completada', key=f"mark_{i}"):
                        mark_task(i)
                with col2:
                    if st.button('Eliminar', key=f"delete_{i}"):
                        delete_task(i)
else:
    st.write('No hay tareas pendientes.')

# Mostrar las tareas completadas
if any(task['completed'] for task in tasks):
    st.write('### Tareas Completadas:')
    for i, task in enumerate(tasks):
        if task['completed']:
            st.write(f"{i + 1}. **{task['text']}** - {task['priority']}")
else:
    st.write('No hay tareas completadas.')