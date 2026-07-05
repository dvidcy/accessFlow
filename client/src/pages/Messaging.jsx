import { useState, useEffect } from 'react';
import api from '../api';

export default function Messaging() {
  const [tipo, setTipo] = useState('individual');
  const [tutors, setTutors] = useState([]);
  const [groups, setGroups] = useState([]);
  const [tutorId, setTutorId] = useState('');
  const [grupoId, setGrupoId] = useState('');
  const [asunto, setAsunto] = useState('');
  const [cuerpo, setCuerpo] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    api.get('/tutors').then(r => setTutors(r.data));
    api.get('/groups').then(r => setGroups(r.data));
  }, []);

  async function handleSend(e) {
    e.preventDefault();
    if (!asunto || !cuerpo) { setResult({ ok: false, msg: 'Asunto y mensaje son requeridos.' }); return; }
    if (tipo === 'individual' && !tutorId) { setResult({ ok: false, msg: 'Selecciona un tutor.' }); return; }
    if (tipo === 'grupal' && !grupoId) { setResult({ ok: false, msg: 'Selecciona un grupo.' }); return; }

    setLoading(true);
    setResult(null);
    try {
      const { data } = await api.post('/messaging/send', {
        tipo, tutor_id: tutorId || undefined, grupo_id: grupoId || undefined, asunto, cuerpo,
      });
      setResult({ ok: true, msg: `Mensaje enviado a ${data.destinatarios} destinatario(s).` });
      setAsunto(''); setCuerpo(''); setTutorId(''); setGrupoId('');
    } catch (err) {
      setResult({ ok: false, msg: err.response?.data?.error ?? 'Error al enviar.' });
    } finally { setLoading(false); }
  }

  return (
    <div>
      <h2 className="text-2xl font-bold mb-5">Mensajes</h2>

      <form onSubmit={handleSend} className="bg-gray-900 p-6 rounded-xl max-w-2xl space-y-4">
        <div className="flex gap-4">
          {['individual', 'grupal'].map(t => (
            <label key={t} className="flex items-center gap-2 cursor-pointer">
              <input type="radio" name="tipo" value={t} checked={tipo === t} onChange={() => setTipo(t)}
                className="accent-blue-500" />
              <span className="capitalize text-sm">{t}</span>
            </label>
          ))}
        </div>

        {tipo === 'individual' ? (
          <div className="flex flex-col gap-1">
            <label className="text-xs text-gray-400">Tutor destinatario</label>
            <select value={tutorId} onChange={e => setTutorId(e.target.value)}
              className="bg-gray-800 text-white rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
              <option value="">{tutors.length ? '— Selecciona —' : 'Sin tutores registrados'}</option>
              {tutors.map(t => <option key={t.id} value={t.id}>{t.nombre} ({t.email})</option>)}
            </select>
          </div>
        ) : (
          <div className="flex flex-col gap-1">
            <label className="text-xs text-gray-400">Grupo destinatario</label>
            <select value={grupoId} onChange={e => setGrupoId(e.target.value)}
              className="bg-gray-800 text-white rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
              <option value="">{groups.length ? '— Selecciona —' : 'Sin grupos registrados'}</option>
              {groups.map(g => <option key={g.id} value={g.id}>{g.grado}° {g.nombre} — {g.turno}</option>)}
            </select>
          </div>
        )}

        <div className="flex flex-col gap-1">
          <label className="text-xs text-gray-400">Asunto</label>
          <input value={asunto} onChange={e => setAsunto(e.target.value)} placeholder="Asunto del mensaje"
            className="bg-gray-800 text-white rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>

        <div className="flex flex-col gap-1">
          <label className="text-xs text-gray-400">Mensaje</label>
          <textarea value={cuerpo} onChange={e => setCuerpo(e.target.value)} rows={5}
            className="bg-gray-800 text-white rounded-lg px-3 py-2 text-sm resize-none focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>

        {result && (
          <p className={`text-sm ${result.ok ? 'text-green-400' : 'text-red-400'}`}>{result.msg}</p>
        )}

        <button type="submit" disabled={loading}
          className="bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white text-sm font-medium px-6 py-2.5 rounded-lg transition-colors">
          {loading ? 'Enviando...' : 'Enviar mensaje'}
        </button>
      </form>
    </div>
  );
}
