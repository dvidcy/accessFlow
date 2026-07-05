import { useState, useEffect } from 'react';
import api from '../api';

const EMPTY = { nombre: '', grupo_id: '', rfid_uid: '' };

export default function Students() {
  const [students, setStudents] = useState([]);
  const [groups, setGroups] = useState([]);
  const [filterGrupo, setFilterGrupo] = useState('');
  const [form, setForm] = useState(EMPTY);
  const [editing, setEditing] = useState(null);
  const [msg, setMsg] = useState(null);

  useEffect(() => { load(); loadGroups(); }, []);

  async function load(grupo_id = '') {
    const { data } = await api.get('/students', { params: grupo_id ? { grupo_id } : {} });
    setStudents(data);
  }

  async function loadGroups() {
    const { data } = await api.get('/groups');
    setGroups(data);
  }

  function flash(text, ok = true) { setMsg({ text, ok }); setTimeout(() => setMsg(null), 3000); }

  async function handleSubmit(e) {
    e.preventDefault();
    if (!form.nombre || !form.grupo_id) { flash('Nombre y grupo son requeridos.', false); return; }
    try {
      if (editing) {
        await api.put(`/students/${editing}`, form);
        flash('Alumno actualizado.');
      } else {
        await api.post('/students', form);
        flash('Alumno agregado.');
      }
      setForm(EMPTY); setEditing(null); load(filterGrupo);
    } catch (err) { flash(err.response?.data?.error ?? 'Error.', false); }
  }

  async function handleDelete(id) {
    if (!confirm('¿Eliminar alumno?')) return;
    await api.delete(`/students/${id}`);
    flash('Alumno eliminado.');
    load(filterGrupo);
  }

  function startEdit(s) {
    setEditing(s.id);
    setForm({ nombre: s.nombre, grupo_id: s.grupo_id, rfid_uid: s.rfid_uid ?? '' });
  }

  return (
    <div>
      <h2 className="text-2xl font-bold mb-5">Alumnos</h2>

      <form onSubmit={handleSubmit} className="bg-gray-900 p-4 rounded-xl mb-4 flex flex-wrap gap-3 items-end">
        <Field label="Nombre" value={form.nombre} onChange={v => setForm(f => ({ ...f, nombre: v }))} placeholder="Nombre completo" />
        <div className="flex flex-col gap-1">
          <label className="text-xs text-gray-400">Grupo</label>
          <select value={form.grupo_id} onChange={e => setForm(f => ({ ...f, grupo_id: e.target.value }))}
            className="bg-gray-800 text-white rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
            <option value="">—</option>
            {groups.map(g => <option key={g.id} value={g.id}>{g.grado}° {g.nombre}</option>)}
          </select>
        </div>
        <Field label="RFID (opcional)" value={form.rfid_uid} onChange={v => setForm(f => ({ ...f, rfid_uid: v }))} placeholder="UID tarjeta" />
        <div className="flex gap-2 items-end">
          <button type="submit" className="bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium px-5 py-2 rounded-lg">
            {editing ? 'Guardar' : 'Agregar'}
          </button>
          {editing && <button type="button" onClick={() => { setEditing(null); setForm(EMPTY); }} className="text-sm text-gray-400 hover:text-white px-3 py-2">Cancelar</button>}
        </div>
        {msg && <span className={`text-sm ${msg.ok ? 'text-green-400' : 'text-red-400'}`}>{msg.text}</span>}
      </form>

      <div className="mb-4 flex items-center gap-3">
        <span className="text-sm text-gray-400">Filtrar por grupo:</span>
        <select value={filterGrupo} onChange={e => { setFilterGrupo(e.target.value); load(e.target.value); }}
          className="bg-gray-800 text-white rounded-lg px-3 py-1.5 text-sm focus:outline-none">
          <option value="">Todos</option>
          {groups.map(g => <option key={g.id} value={g.id}>{g.grado}° {g.nombre}</option>)}
        </select>
      </div>

      <div className="bg-gray-900 rounded-xl overflow-hidden">
        <div className="grid grid-cols-6 bg-gray-800 px-4 py-2.5 text-xs font-semibold text-gray-400 uppercase tracking-wide">
          <span>ID</span><span>Nombre</span><span>Grupo</span><span>Turno</span><span>RFID</span><span>Acciones</span>
        </div>
        {students.length === 0 ? (
          <p className="text-center text-gray-500 py-8 text-sm">Sin alumnos.</p>
        ) : students.map(s => (
          <div key={s.id} className="grid grid-cols-6 px-4 py-3 border-t border-gray-800 text-sm hover:bg-gray-800/50 items-center">
            <span className="text-gray-400">{s.id}</span>
            <span>{s.nombre}</span>
            <span>{s.Grupo?.grado}° {s.Grupo?.nombre}</span>
            <span className="capitalize">{s.Grupo?.turno}</span>
            <span className="text-gray-400">{s.rfid_uid ?? '—'}</span>
            <div className="flex gap-2">
              <button onClick={() => startEdit(s)} className="text-blue-400 hover:text-blue-300 text-xs">Editar</button>
              <button onClick={() => handleDelete(s.id)} className="text-red-400 hover:text-red-300 text-xs">Eliminar</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function Field({ label, value, onChange, placeholder }) {
  return (
    <div className="flex flex-col gap-1">
      <label className="text-xs text-gray-400">{label}</label>
      <input value={value} onChange={e => onChange(e.target.value)} placeholder={placeholder}
        className="bg-gray-800 text-white rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
    </div>
  );
}
