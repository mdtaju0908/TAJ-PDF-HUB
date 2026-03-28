# Smart PDF Tools - Deployment Guide

This guide covers the complete deployment process for the Smart PDF Tools full-stack application.

## 📁Project Structure

```
TAJ-PDF-Docs/
├── backend/
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── Procfile
│   ├── README.md
│   ├── requirements.txt
│   └── app/
│       ├── main.py
│       ├── api/
│       │   ├── deps.py
│       │   └── routes/
│       │       ├── compress.py
│       │       ├── convert.py
│       │       ├── edit.py
│       │       ├── merge.py
│       │       ├── ocr.py
│       │       ├── split.py
│       │       └── tools.py
│       ├── core/
│       │   ├── config.py
│       │   └── security.py
│       ├── models/
│       │   └── schemas.py
│       ├── services/
│       │   ├── compress_service.py
│       │   ├── convert_service.py
│       │   ├── crop_pdf_service.py
│       │   ├── edit_service.py
│       │   ├── excel_to_pdf_service.py
│       │   ├── html_to_pdf_service.py
│       │   ├── merge_service.py
│       │   ├── ocr_service.py
│       │   ├── organize_pdf_service.py
│       │   ├── pdf_to_excel_service.py
│       │   ├── pdf_to_ppt_service.py
│       │   ├── redact_pdf_service.py
│       │   ├── repair_pdf_service.py
│       │   ├── scan_to_pdf_service.py
│       │   ├── sign_pdf_service.py
│       │   ├── split_service.py
│       │   └── word_to_pdf_service.py
│       └── utils/
│           ├── file_handler.py
│           ├── response.py
│           ├── s3_client.py
│           └── s3.py
└── frontend/
    ├── API-USAGE.md
    ├── DEPLOYMENT.md
    ├── next-env.d.ts
    ├── next.config.mjs
    ├── package.json
    ├── postcss.config.js
    ├── SECURITY.md
    ├── tailwind.config.js
    ├── tsconfig-next14.json
    ├── tsconfig.json
    ├── app/
    │   ├── error.tsx
    │   ├── globals.css
    │   ├── layout.tsx
    │   ├── loading.tsx
    │   ├── page.tsx
    │   ├── sitemap.ts
    │   ├── about/
    │   │   └── page.tsx
    │   ├── api/
    │   │   └── [tool]/
    │   │       └── route.ts
    │   ├── dashboard/
    │   │   ├── layout.tsx
    │   │   ├── page.tsx
    │   │   ├── favorites/
    │   │   │   └── page.tsx
    │   │   ├── recent/
    │   │   │   └── page.tsx
    │   │   └── security/
    │   │       └── page.tsx
    │   ├── features/
    │   │   └── page.tsx
    │   ├── help/
    │   │   └── page.tsx
    │   ├── security/
    │   │   └── page.tsx
    │   └── tools/
    │       └── [tool]/
    │           └── page.tsx
    ├── components/
    │   ├── FeatureGrid.tsx
    │   ├── FilePreview.tsx
    │   ├── Footer.tsx
    │   ├── Navbar.tsx
    │   ├── PdfToolTemplate.tsx
    │   ├── PremiumPreview.tsx
    │   ├── SidebarMenu.tsx
    │   ├── ToolCard.tsx
    │   ├── UploadBox.tsx
    │   ├── panels/
    │   │   ├── CompressPanel.tsx
    │   │   ├── EditPanel.tsx
    │   │   ├── MergePanel.tsx
    │   │   ├── NumberingPanel.tsx
    │   │   ├── OCRPanel.tsx
    │   │   ├── ProtectPanel.tsx
    │   │   ├── RotatePanel.tsx
    │   │   ├── SplitPanel.tsx
    │   │   ├── UnlockPanel.tsx
    │   │   └── WatermarkPanel.tsx
    │   └── ui/
    │       ├── button.tsx
    │       ├── card.tsx
    │       ├── ErrorMessage.tsx
    │       └── Loader.tsx
    └── lib/
        ├── api-config.ts
        ├── api.ts
        ├── store.ts
        ├── tools.ts
        └── utils.ts
```