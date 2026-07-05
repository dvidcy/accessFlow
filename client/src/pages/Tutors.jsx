import { useState, useEffect } from 'react';
import api from '../api';

const EMPTY = { nombre: '', email: '', telefono: '', alumno_id: '', parentesco: '' };

export default function Tutors() {
  const [tutors, setTutors] = useState([]);
  const [students, setStudents] = useState([]);
  const [form, setForm] = useState(EMPTY);
  const [editing, setEditing] = useState(null);
  const [msg, setMsg] = useState(null);

  useEffect(() => { load(); loadStudents(); }, []);

  async function load() { const { data } = await api.get('/tutors'); setTutors(data); }
  async function loadStudents() { const { data } = await api.get('/students'); setStudents(data); }

  function flash(text, ok = true) { setMsg({ text, ok }); setTimeout(() => setMsg(null), 3000); }
  function set(k) { return e => setForm(f => ({ ...f, [k]: e.target.value })); }

  async function handleSubmit(e) {
    e.preventDefault();
    if (!form.nombre || !form.email) { flash('Nombre y email son requeridos.', false); return; }
    try {
      if (editing) { await api.put(`/tutors/${editing}`, form); flash('Tutor actualizado.'); }
      else { await api.post('/tutors', form); flash('Tutor agregado.'); }
      setForm(EMPTY); setEditing(null); load();
    } catch (err) { flash(err.response?.data?.error ?? 'Error.', false); }
  }

  async function handleDelete(id) {
    if (!confirm('¿Eliminar tutor?')) return;
    await api.delete(`/tutors/${id}`); flash('Tutor eliminado.'); load();
  }

  function startEdit(t) {
    setEditing(t.id);
    setForm({ nombre: t.nombre, email: t.email, telefono: t.telefono ?? '', alumno_id: '', parentesco: '' });
  }

  return (
    <div>
      <h2 className="text-2xl font-bold mb-5">Tutores</h2>

      <form onSubmit={handleSubmit} className="bg-gray-900 p-4 rounded-xl mb-6 space-y-3">
        <div className="flex flex-wrap gap-3">
          <Input label="Nombre" value={form.nombre} onChange={set('nombre')} placeholder="Nombre completo" w="w-44" />
          <Input label="Email" value={form.email} onChange={set('email')} placeholder="correo@ejemplo.com" w="w-52" />
          <Input label="Teléfono" value={form.telefono} onChange={set('telefono')} placeholder="Opcional" w="w-32" />
        </div>
        {!editing && (
          <div className="flex flex-wrap gap-3">
            <div className="flex flex-col gap-1">
              <label className="text-xs text-gray-400">Alumno</label>
              <select value={form.alumno_id} onChange={set('alumno_id')}
                className="bg-gray-800 text-white rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 w-44">
                <option value="">— Opcional —</option>
                {students.map(s => <option key={s.id} value={s.id}>{s.nombre}</option>)}
              </select>
            </div>
            <Input label="Parentesco" value={form.parentesco} onChange={set('parentesco')} placeholder="madre / padre..." w="w-36" />
          </div>
        )}
        <div className="flex gap-2 items-center">
          <button type="submit" className="bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium px-5 py-2 rounded-lg">
            {editing ? 'Guardar' : 'Agregar tutor'}
          </button>
          {editing && <button type="button" onClick={() => { setEditing(null); setForm(EMPTY); }} className="text-sm text-gray-400 hover:text-white px-3 py-2">Cancelar</button>}
          {msg && <span className={`text-sm ${msg.ok ? 'text-green-400' : 'text-red-400'}`}>{msg.text}</span>}
        </div>
      </form>

      <div className="bg-gray-900 rounded-xl overflow-hidden">
        <div className="grid grid-cols-6 bg-gray-800 px-4 py-2.5 text-xs font-semibold text-gray-400 uppercase tracking-wide">
          <span>ID</span><span>Nombre</span><span>Email</span><span>Teléfono</span><span>Alumnos</span><span>Acciones</span>
        </div>
        {tutors.length === 0 ? (
          <p className="text-center text-gray-500 py-8 text-sm">Sin tutores.</p>
        ) : tutors.map(t => (
          <div key={t.id} className="grid grid-cols-6 px-4 py-3 border-t border-gray-800 text-sm hover:bg-gray-800/50 items-center">
            <span className="text-gray-400">{t.id}</span>
            <span>{t.nombre}</span>
            <span className="text-gray-300">{t.email}</span>
            <span className="text-gray-400">{t.telefono ?? '—'}</span>
            <span className="text-gray-400 text-xs">{t.Alumnos?.map(a => a.nombre).join(', ') || '—'}</span>
            <div className="flex gap-2">
              <button onClick={() => startEdit(t)} className="text-blue-400 hover:text-blue-300 text-xs">Editar</button>
              <button onClick={() => handleDelete(t.id)} className="text-red-400 hover:text-red-300 text-xs">Eliminar</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function Input({ label, value, onChange, placeholder, w = 'w-40' }) {
  return (
    <div className="flex flex-col gap-1">
      <label className="text-xs text-gray-400">{label}</label>
      <input value={value} onChange={onChange} placeholder={placeholder}
        className={`bg-gray-800 text-white rounded-lg px-3 py-2 text-sm ${w} focus:outline-none focus:ring-2 focus:ring-blue-500`} />
    </div>
  );
}
