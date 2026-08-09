# 🏢 Headless Real Estate ERP & CRM

Una solución de gestión inmobiliaria de extremo a extremo que separa una experiencia web ultrarrápida de un robusto panel de control empresarial.

## 🚀 Arquitectura
Este proyecto utiliza una arquitectura *Headless* compuesta por dos módulos principales:
- **Frontend (Web):** Construido con **Svelte**, ofreciendo una interfaz de usuario reactiva, moderna y de carga instantánea para la exhibición de propiedades.
- **Backend (ERP/CRM):** Servidor personalizado de **Odoo 17** corriendo en **Docker** (junto a PostgreSQL), que expone una API REST para el frontend.

## ✨ Características Principales
- **Sincronización en tiempo real:** Las propiedades marcadas como "Vendidas" o "Reservadas" en el ERP desaparecen del frontend automáticamente.
- **Captación de Leads (CRM):** Los formularios web se inyectan directamente en el tablero Kanban de Odoo, asignando el lead automáticamente al asesor correspondiente.
- **Alertas Omnicanal:** Integración nativa con la API de **WhatsApp Cloud (Meta)** para notificar a los asesores instantáneamente sobre nuevos prospectos.
- **Seguridad y Permisos:** Control de acceso por roles (Asesor vs. Administrador) utilizando las Record Rules de Odoo.

## 🛠️ Tecnologías Utilizadas
- **Frontend:** Svelte, HTML5, CSS3, JavaScript.
- **Backend:** Python, Odoo, PostgreSQL, Docker, Docker Compose.
- **Integraciones:** WhatsApp Cloud API (Meta for Developers).
