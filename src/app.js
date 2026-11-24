{
  /* Cấu hình: dán URL Google Apps Script vào đây để form báo giá đổ về Google Sheet */
  const FORM_ENDPOINT = "";

  const burger = document.querySelector(".burger");
  const menu = document.querySelector(".menu");
  if (burger && menu) {
    burger.addEventListener("click", () => {
      const open = menu.classList.toggle("open");
      burger.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  /* Video: chỉ tải YouTube khi khách bấm, giúp trang mở nhanh */
  document.querySelectorAll(".video").forEach((v) => {
    v.addEventListener("click", () => {
      const id = v.dataset.yt;
      if (!id) {
        if (!v.querySelector(".note")) {
          const n = document.createElement("div");
          n.className = "note";
          n.textContent = "Clip xưởng đang được cập nhật. Gọi 0989 139 333 để xem mẫu thật tại xưởng.";
          v.appendChild(n);
        }
        return;
      }
      const f = document.createElement("iframe");
      f.src = "https://www.youtube-nocookie.com/embed/" + encodeURIComponent(id) + "?autoplay=1&rel=0";
      f.title = v.dataset.title || "Video";
      f.allow = "autoplay; encrypted-media; picture-in-picture";
      f.allowFullscreen = true;
      v.replaceChildren(f);
    });
  });

  /* Google Map: tải bản đồ khi khách bấm "Xem bản đồ" */
  document.querySelectorAll("[data-map]").forEach((b) => {
    b.addEventListener("click", () => {
      const box = document.querySelector(".map .art");
      if (!box || box.querySelector("iframe")) return;
      const f = document.createElement("iframe");
      f.src = b.dataset.map;
      f.title = "Bản đồ xưởng Tâm Tín Phát";
      f.loading = "lazy";
      f.referrerPolicy = "no-referrer-when-downgrade";
      box.appendChild(f);
      b.remove();
    });
  });

  /* Form báo giá */
  document.querySelectorAll("form.quote").forEach((form) => {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const ok = form.querySelector(".ok");
      const data = Object.fromEntries(new FormData(form).entries());
      data.trang = location.pathname;
      data.thoi_gian = new Date().toISOString();
      try {
        const p = new URLSearchParams(location.search);
        ["utm_source", "utm_medium", "utm_campaign", "gclid", "fbclid"].forEach((k) => { if (p.get(k)) data[k] = p.get(k); });
      } catch (err) {}
      let sent = false;
      if (FORM_ENDPOINT) {
        try {
          await fetch(FORM_ENDPOINT, { method: "POST", mode: "no-cors", body: JSON.stringify(data) });
          sent = true;
        } catch (err) {}
      }
      if (window.dataLayer) window.dataLayer.push({ event: "gui_bao_gia", nhom: data.nhom || "" });
      ok.textContent = sent
        ? "Đã nhận yêu cầu của anh/chị. Nhân viên Tâm Tín Phát sẽ gọi lại sớm."
        : "Bản thử: yêu cầu chưa được gửi đi. Anh/chị vui lòng gọi 0989 139 333 hoặc nhắn Zalo 0961 232 277.";
      ok.classList.add("show");
      if (sent) form.reset();
    });
  });

  /* Lọc bảng mã / máy */
  document.querySelectorAll(".filters").forEach((f) => {
    const box = document.getElementById(f.dataset.target);
    if (!box) return;
    const items = () => box.querySelectorAll("tbody tr, .dev");
    let grp = "all";
    const q = f.querySelector(".fsearch");
    const norm = (t) => t.toLowerCase().replace(/[×x*]/g, "x").replace(/\s+/g, "");
    const apply = () => {
      const k = q ? norm(q.value) : "";
      items().forEach((it) => {
        const okG = grp === "all" || it.dataset.g === grp;
        const okQ = !k || norm(it.textContent).includes(k);
        it.classList.toggle("hide", !(okG && okQ));
      });
    };
    f.querySelectorAll(".fchip").forEach((c) => c.addEventListener("click", () => {
      f.querySelectorAll(".fchip").forEach((x) => x.classList.remove("on"));
      c.classList.add("on"); grp = c.dataset.f; apply();
    }));
    if (q) q.addEventListener("input", apply);
  });

  /* Thư viện ảnh: nút trước/sau và phím mũi tên */
  document.querySelectorAll(".gbtn").forEach((btn) => btn.addEventListener("click", () => {
    const g = document.getElementById(btn.dataset.g);
    if (g) g.scrollBy({ left: Number(btn.dataset.d) * g.clientWidth * 0.8, behavior: "smooth" });
  }));
  document.querySelectorAll(".gal").forEach((g) => g.addEventListener("keydown", (ev) => {
    if (ev.key === "ArrowRight") g.scrollBy({ left: g.clientWidth * 0.8, behavior: "smooth" });
    if (ev.key === "ArrowLeft") g.scrollBy({ left: -g.clientWidth * 0.8, behavior: "smooth" });
  }));

  /* Đo bấm gọi / Zalo cho quảng cáo */
  document.querySelectorAll("a[href^='tel:'],a[href*='zalo.me']").forEach((a) => {
    a.addEventListener("click", () => {
      if (window.dataLayer) window.dataLayer.push({ event: a.href.startsWith("tel:") ? "bam_goi" : "bam_zalo" });
    });
  });
}
