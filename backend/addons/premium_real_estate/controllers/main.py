from odoo import http  # type: ignore
from odoo.http import request  # type: ignore
import json
import requests # type: ignore
from datetime import datetime, timedelta

class RealEstateController(http.Controller):

    @http.route('/api/contacto', type='http', auth='public', methods=['POST'], csrf=False, cors='*')
    def crear_contacto(self, **kwargs):
        try:
            datos = json.loads(request.httprequest.data)
            email_cliente = datos.get('email')
            nombre_cliente = datos.get('firstName', '')
            
            # --- 1. SEGURIDAD: Protección Anti-Spam (Rate Limiting) ---
            # Buscamos si existe un lead creado con este email en los últimos 10 minutos
            tiempo_limite = datetime.now() - timedelta(minutes=10)
            lead_existente = request.env['crm.lead'].sudo().search_count([
                ('email_from', '=', email_cliente),
                ('create_date', '>=', tiempo_limite.strftime('%Y-%m-%d %H:%M:%S'))
            ])

            if lead_existente > 0:
                respuesta = {
                    'status': 429, 
                    'message': 'Hemos recibido tu solicitud recientemente. Por favor, espera unos minutos antes de intentar de nuevo.'
                }
                return request.make_response(json.dumps(respuesta), headers=[('Content-Type', 'application/json')])

            # --- 2. CREACIÓN EN CRM ---
            nombre_completo = f"{nombre_cliente} {datos.get('lastName', '')}"
            
            # Buscamos automáticamente las etiquetas por su nombre. 
            # Cambia 'Web' y 'Nuevo' por los nombres exactos que hayas creado en Odoo.
            etiquetas = request.env['crm.tag'].sudo().search([
                ('name', 'in', ['Web', 'Nuevo']) 
            ])
            
            nuevo_lead = request.env['crm.lead'].sudo().create({
                'name': f"Interesado Web: {nombre_completo}",
                'contact_name': nombre_completo,
                'email_from': email_cliente,
                'phone': datos.get('phone'),
                'description': 'Llegó desde el formulario de contacto web.',
                # NUEVO: Asignación automática al asesor (cambia el 6 por el ID real de Carlos)
                'user_id': 8, 
                # NUEVO: Vinculamos las etiquetas encontradas
                'tag_ids': [(6, 0, etiquetas.ids)] if etiquetas else False
            })

            # --- 3. ENVÍO DE CORREO AUTOMÁTICO (Plantilla Estilizada) ---
            # Diseñamos un HTML responsivo, con colores acordes a tu frontend (Azul #2563eb y grises elegantes)
            html_body = f"""
            <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; overflow: hidden; border: 1px solid #e5e7eb; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                <div style="background-color: #2563eb; padding: 30px; text-align: center;">
                    <h1 style="color: #ffffff; margin: 0; font-size: 24px; font-weight: 700; letter-spacing: 1px;">PREMIUM REAL ESTATE</h1>
                </div>
                <div style="padding: 40px 30px;">
                    <h2 style="color: #1f2937; font-size: 20px; margin-top: 0;">¡Hola, {nombre_cliente}!</h2>
                    <p style="color: #4b5563; font-size: 16px; line-height: 1.6; margin-bottom: 20px;">
                        Gracias por contactar con <strong>Premium Real Estate</strong>. Te informamos que hemos recibido tu solicitud exitosamente y nuestro equipo ya está trabajando en ella.
                    </p>
                    <p style="color: #4b5563; font-size: 16px; line-height: 1.6; margin-bottom: 30px;">
                        Un agente especializado se estará comunicando contigo próximamente al número que nos proporcionaste. Mientras tanto, te invitamos a explorar nuestro catálogo de propiedades exclusivas o seguir nuestras redes sociales.
                    </p>
                    <div style="text-align: center;">
                        <a href="http://localhost:5173" style="display: inline-block; background-color: #2563eb; color: #ffffff; text-decoration: none; padding: 12px 28px; border-radius: 8px; font-weight: bold; font-size: 16px;">Ver Catálogo de Propiedades</a>
                    </div>
                </div>
                <div style="background-color: #f9fafb; padding: 20px; text-align: center; border-top: 1px solid #e5e7eb;">
                    <p style="color: #6b7280; font-size: 14px; margin: 0 0 10px 0;">
                        Descubre tu próximo hogar con nosotros.
                    </p>
                    <p style="color: #9ca3af; font-size: 11px; margin: 0;">
                        Este es un correo generado automáticamente. Por favor, no respondas a esta dirección (no-reply).
                    </p>
                </div>
            </div>
            """

            mail_values = {
                'subject': 'Hemos recibido tu solicitud - Premium Real Estate',
                'email_to': email_cliente,
                'email_from': 'no-reply@premiumrealestate.com',
                'body_html': html_body,
            }
            
            # Odoo crea y pone el correo en la cola de salida inmediatamente
            request.env['mail.mail'].sudo().create(mail_values).send()
            # --- 5. ALERTA POR WHATSAPP AL ASESOR ---
            # Tu número personal para recibir las alertas (sin el '+' y con código de país, ej: 584120000000)
            numero_asesor = 'TU_NUMERO_AQUI' 
            
            mensaje_whatsapp = (
                f"🏠 *Nuevo Cliente Potencial*\n\n"
                f"👤 *Nombre:* {nombre_completo}\n"
                f"📞 *Teléfono:* {datos.get('phone')}\n"
                f"✉️ *Correo:* {email_cliente}\n\n"
                f"¡Entra al CRM de Odoo para contactarlo!"
            )

            # Credenciales de Meta (WhatsApp Cloud API)
            whatsapp_token = 'TU_TOKEN_DE_META'
            id_telefono_origen = 'TU_PHONE_ID'

            url_wa = f'https://graph.facebook.com/v17.0/{id_telefono_origen}/messages'
            headers_wa = {
                'Authorization': f'Bearer {whatsapp_token}',
                'Content-Type': 'application/json'
            }
            payload_wa = {
                "messaging_product": "whatsapp",
                "to": numero_asesor,
                "type": "text",
                "text": {"body": mensaje_whatsapp}
            }

            try:
                # Hacemos la petición a la API de WhatsApp, pero le ponemos un timeout 
                # para que si WhatsApp falla temporalmente, la página web no se quede colgada.
                requests.post(url_wa, headers=headers_wa, json=payload_wa, timeout=5)
            except Exception as e:
                # Si hay error con WhatsApp, lo imprimimos en consola pero no rompemos el formulario
                print(f"Error silencioso al enviar WhatsApp: {e}")
            # --- 4. RESPUESTA AL FRONTEND ---
            respuesta = {'status': 200, 'message': 'Contacto creado y correo enviado', 'lead_id': nuevo_lead.id}
            return request.make_response(json.dumps(respuesta), headers=[('Content-Type', 'application/json')])

        except Exception as e:
            return request.make_response(json.dumps({'status': 500, 'message': str(e)}), headers=[('Content-Type', 'application/json')])

    # 2. NUEVA RUTA: OBTENER PROPIEDADES PARA EL CARRUSEL
    @http.route('/api/propiedades', type='http', auth='public', methods=['GET'], csrf=False, cors='*')
    def obtener_propiedades(self, **kwargs):
        try:
            # Buscamos solo las propiedades que estén activas Y disponibles
            propiedades = request.env['premium.property'].sudo().search_read(
                [('active', '=', True), ('state', '=', 'disponible')],
                ['id', 'name', 'price', 'desc', 'img_url', 'location', 'beds', 'baths', 'parking', 'long_desc']
            )
            
            # Las formateamos para que Svelte las reciba exactamente con los mismos nombres
            resultado = []
            for p in propiedades:
                resultado.append({
                    'id': p['id'],
                    'title': p['name'],
                    'price': p['price'],
                    'desc': p['desc'],
                    'img': p['img_url'],
                    'location': p['location'],
                    'beds': p['beds'],
                    'baths': p['baths'],
                    'parking': p['parking'],
                    'longDesc': p['long_desc']
                })

            respuesta = {'status': 200, 'data': resultado}
            return request.make_response(json.dumps(respuesta), headers=[('Content-Type', 'application/json')])
        except Exception as e:
            return request.make_response(json.dumps({'status': 500, 'message': str(e)}), headers=[('Content-Type', 'application/json')])