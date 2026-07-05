import { useState, useEffect } from 'react';
import api from '../api';

const EMPTY = { nombre: '', grado: '', turno: 'matutino' };
const TURNOS = ['matutino', 'vespertino', 'nocturno'];

export default function Groups() {
  const [groups, setGroups] = useState([]);
  const [form, setForm] = useState(EMPTY);
  const [editing, setEditing] = useState(null);
  const [msg, setMsg] = useState(null);

  useEffect(() => { load(); }, []);

  async function load() { const { data } = await api.get('/groups'); setGroups(data); }

  function flash(text, ok = true) { setMsg({ text, ok }); setTimeout(() => setMsg(null), 3000); }

  async function handleSubmit(e) {
    e.preventDefault();
    if (!form.nombre || !form.grado) { flash('Nombre y grado son requeridos.', false); return; }
    if (isNaN(form.grado)) { flash('Grado debe ser un número.', false); return; }
    try {
      if (editing) { await api.put(`/groups/${editing}`, form); flash('Grupo actualizado.'); }
      else { await api.post('/groups', form); flash('Grupo agregado.'); }
      setForm(EMPTY); setEditing(null); load();
    } catch (err) { flash(err.response?.data?.error ?? 'Error.', false); }
  }

  async function handleDelete(id) {
    if (!confirm('¿Eliminar grupo?')) return;
    try { await api.delete(`/groups/${id}`); flash('Grupo eliminado.'); load(); }
    catch (err) { flash(err.response?.data?.error ?? 'Error.', false); }
  }

  function startEdit(g) { setEditing(g.id); setForm({ nombre: g.nombre, grado: String(g.grado), turno: g.turno }); }

  return (
    <div>
      <h2 className="text-2xl font-bold mb-5">Grupos</h2>

      <form onSubmit={handleSubmit} className="bg-gray-900 p-4 rounded-xl mb-6 flex flex-wrap gap-3 items-end">
        <div className="flex flex-col gap-1">
          <label className="text-xs text-gray-400">Nombre</label>
          <input value={form.nombre} onChange={e => setForm(f => ({ ...f, nombre: e.target.value }))} placeholder="1A"
            className="bg-gray-800 text-white rounded-lg px-3 py-2 text-sm w-24 focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>
        <div className="flex flex-col gap-1">
          <label className="text-xs text-gray-400">Grado</label>
          <input value={form.grado} onChange={e => setForm(f => ({ ...f, grado: e.target.value }))} placeholder="1"
            className="bg-gray-800 text-white rounded-lg px-3 py-2 text-sm w-20 focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>
        <div className="flex flex-col gap-1">
          <label className="text-xs text-gray-400">Turno</label>
          <select value={form.turno} onChange={e => setForm(f => ({ ...f, turno: e.target.value }))}
            className="bg-gray-800 text-white rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
            {TURNOS.map(t => <option key={t} value={t}>{t}</option>)}
          </select>
        </div>
        <div className="flex gap-2 items-end">
          <button type="submit" className="bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium px-5 py-2 rounded-lg">
            {editing ? 'Guardar' : 'Agregar grupo'}
          </button>
          {editing && <button type="button" onClick={() => { setEditing(null); setForm(EMPTY); }} className="text-sm text-gray-400 hover:text-white px-3 py-2">Cancelar</button>}
        </div>
        {msg && <span className={`text-sm ${msg.ok ? 'text-green-400' : 'text-red-400'}`}>{msg.text}</span>}
      </form>

      <div className="bg-gray-900 rounded-xl overflow-hidden">
        <div className="grid grid-cols-5 bg-gray-800 px-4 py-2.5 text-xs font-semibold text-gray-400 uppercase tracking-wide">
          <span>ID</span><span>Nombre</span><span>Grado</span><span>Turno</span><span>Acciones</span>
        </div>
        {groups.length === 0 ? (
          <p className="text-center text-gray-500 py-8 text-sm">Sin grupos.</p>
        ) : groups.map(g => (
          <div key={g.id} className="grid grid-cols-5 px-4 py-3 border-t border-gray-800 text-sm hover:bg-gray-800/50 items-center">
            <span className="text-gray-400">{g.id}</span>
            <span>{g.nombre}</span>
            <span>{g.grado}°</span>
            <span className="capitalize">{g.turno}</span>
            <div className="flex gap-2">
              <button onClick={() => startEdit(g)} className="text-blue-400 hover:text-blue-300 text-xs">Editar</button>
              <button onClick={() => handleDelete(g.id)} className="text-red-400 hover:text-red-300 text-xs">Eliminar</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
