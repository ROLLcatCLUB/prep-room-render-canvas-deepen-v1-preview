// 1013K_R12 readonly client fetch fixture.
// Fixture only: not mounted into the main frontend and not connected to runtime.
export async function fetchBigUnitPreviewViewModel({ viewmodelId, chunkId, fetchImpl = fetch }) {
  const encodedId = encodeURIComponent(viewmodelId);
  const url = new URL(`/api/prep-room/big-unit-preview-viewmodel/${encodedId}`, window.location.origin);
  if (chunkId) {
    url.searchParams.set('chunk_id', chunkId);
  }
  const response = await fetchImpl(url.toString(), { method: 'GET' });
  const payload = await response.json();
  return {
    ok: response.ok && payload.ok === true,
    status: response.status,
    mode: payload.response_mode || 'readonly_error',
    viewmodel: payload.viewmodel || null,
    chunk: payload.chunk || null,
    renderQueue: payload.render_queue || [],
    teacherVisibleMessage: payload.teacher_visible_message || '',
    previewOnly: payload.boundary?.preview_only === true,
    formalApplyPerformed: payload.formal_apply_performed === true,
  };
}

export const bigUnitPreviewFetchExamples1013K_R12 = {
  full: { viewmodelId: 'big_unit_render_viewmodel_fixture_1013K_R7' },
  singleChunk: { viewmodelId: 'big_unit_render_viewmodel_fixture_1013K_R7', chunkId: 'render_chunk_curriculum_basis_1013K_R3' },
  missingChunk: { viewmodelId: 'big_unit_render_viewmodel_fixture_1013K_R7', chunkId: 'missing_chunk_for_error_fixture' },
};
