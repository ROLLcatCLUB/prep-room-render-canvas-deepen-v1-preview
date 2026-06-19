
      (function () {
        function runR6P() {
          const dataNode = document.getElementById("r6p-section-edit-data");
          const scene = document.querySelector("[data-r6p-section-edit-surface]");
          if (!dataNode || !scene) return;
          const sections = JSON.parse(dataNode.textContent || "[]");
          const byId = Object.fromEntries(sections.map((item) => [item.id, item]));
          const docSections = Array.from(scene.querySelectorAll(".nb-doc[data-r6o-field-render-doc='true'] .nb-doc-section"));
          docSections.forEach((sectionEl, index) => {
            const info = sections[index];
            if (!info) return;
            sectionEl.setAttribute("data-r6p-editable-section", info.id);
            const head = sectionEl.querySelector(".nb-doc-section-head");
            if (!head || head.querySelector(".r6p-section-actions")) return;
            const actions = document.createElement("span");
            actions.className = "r6p-section-actions";
            actions.innerHTML = '<button class="node-action secondary" type="button" data-r6p-view="' + info.id + '">查看</button><button class="node-action secondary" type="button" data-r6p-edit="' + info.id + '">编辑</button>';
            const old = head.querySelector('button[data-pending]');
            if (old) old.remove();
            head.appendChild(actions);
          });
          function renderPanel(id, mode) {
            const item = byId[id] || sections[1];
            const impact = item.impact.map((text) => "<li>" + text + "</li>").join("");
            const backdrop = document.querySelector(".r6p-modal-backdrop");
            const title = backdrop.querySelector(".r6p-modal-title");
            const body = backdrop.querySelector(".r6p-modal-body");
            title.textContent = (mode === "view" ? "查看 · " : "正在修改 · ") + item.title;
            if (mode === "view") {
              body.innerHTML = '<div class="r6p-modal-block"><strong>章节说明</strong><p>' + item.view_note + '</p></div><div class="r6p-modal-block"><strong>可能影响</strong><ul>' + impact + '</ul></div><details class="r6p-modal-block"><summary>来源依据</summary><p>依据当前大单元阅读面和候选字段归档，只作为静态预览参考。</p></details>';
            } else {
              body.innerHTML = '<div class="r6p-modal-block"><strong>当前内容</strong><p>' + item.current + '</p></div><div class="r6p-modal-block"><strong>小教建议</strong><p>' + item.suggestion + '</p><p class="r6s-teacher-intent">老师意图：' + (item.teacher_intent || "调整这一段") + '</p></div><div class="r6p-modal-block"><strong>修改前 / 修改后</strong><div class="r6p-modal-compare"><div class="r6p-modal-compare-box"><strong>修改前</strong><p>' + item.before + '</p></div><div class="r6p-modal-compare-box r6s-candidate-box"><strong>修改后 · 候选预览</strong><p>' + item.after + '</p></div></div></div><div class="r6p-modal-block"><strong>为什么这样改</strong><p>' + (item.why_this_change || "让这一段更适合教师阅读和后续单课继承。") + '</p></div><div class="r6p-modal-block"><strong>影响与操作</strong><ul>' + impact + '</ul><p class="r6s-risk-note">' + (item.risk_note || "仅进入本段预览，教师确认前不生效。") + '</p><div class="r6p-modal-actions"><button class="node-action primary" type="button" data-preview-only="true" data-r6s-action="accept_to_section_preview">采纳到本段预览</button><button class="node-action secondary" type="button" data-preview-only="true" data-r6s-action="revise_candidate">继续精修</button><button class="node-action secondary" type="button" data-preview-only="true" data-r6s-action="reject_candidate_for_now">暂不处理</button></div></div><details class="r6p-modal-block"><summary>来源依据</summary><p>候选来自 R6R 静态候选包，依据当前大单元阅读面、教师可见字段模型和后端候选映射归档，只作为静态预览参考。</p></details>';
            }
            backdrop.classList.add("is-open");
            backdrop.setAttribute("aria-hidden", "false");
          }
          scene.addEventListener("click", function (event) {
            const view = event.target.closest("[data-r6p-view]");
            const edit = event.target.closest("[data-r6p-edit]");
            if (view) renderPanel(view.getAttribute("data-r6p-view"), "view");
            if (edit) renderPanel(edit.getAttribute("data-r6p-edit"), "edit");
          });
        }
        if (document.readyState === "loading") {
          document.addEventListener("DOMContentLoaded", () => setTimeout(runR6P, 0));
        } else {
          setTimeout(runR6P, 0);
        }
      })();
    