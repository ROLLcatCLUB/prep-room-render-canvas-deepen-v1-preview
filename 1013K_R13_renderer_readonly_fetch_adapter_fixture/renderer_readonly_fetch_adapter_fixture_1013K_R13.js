// 1013K_R13 renderer readonly fetch adapter fixture.
// Fixture only: not mounted into the main frontend and not connected to runtime.
export function adaptBigUnitViewModelResponseToRenderState(payload) {
  if (!payload || payload.ok !== true) {
    return {
      ok: false,
      mode: 'readonly_error',
      teacherVisibleMessage: payload?.teacher_visible_message || '暂时无法读取这份大单元预览。',
      previewOnly: true,
      chunks: [],
      renderQueue: [],
    };
  }
  if (payload.chunk) {
    return {
      ok: true,
      mode: 'single_chunk',
      previewOnly: payload.boundary?.preview_only !== false,
      chunks: [payload.chunk],
      renderQueue: [payload.chunk.chunk_id],
      replaceChunkId: payload.chunk.chunk_id,
    };
  }
  const viewmodel = payload.viewmodel || {};
  return {
    ok: true,
    mode: 'full_viewmodel',
    previewOnly: payload.boundary?.preview_only !== false,
    documentHeader: viewmodel.document_header || null,
    chunks: viewmodel.section_chunks || [],
    renderQueue: payload.render_queue || viewmodel.render_queue || [],
    chunkCount: payload.chunk_count || (viewmodel.section_chunks || []).length,
  };
}

export const bigUnitRendererAdapterContract1013K_R13 = {
  viewmodelId: 'big_unit_render_viewmodel_fixture_1013K_R7',
  progressiveRenderingSupported: true,
  singleChunkUpdateSupported: true,
  wholeDocumentBlobRequired: false,
};
