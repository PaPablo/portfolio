INFOCUEANEXO = """
select
est.cue || loc.anexo as "Cueanexo",
upper(loc.nombre) as "Nombre",
loc.codigo_jurisdiccional as "Nro",
loc.telefono as "Teléfono",
lower(loc.email) as "Correo electrónico",
initcap(domicilio.calle) || ' ' || domicilio.nro as "Dirección",
domicilio.localidad as "Localidad",
ambito_tipo.descripcion as "Ámbito",
sector_tipo.descripcion as "Sector",
loc_campo_prov_valor.valor as "Región",
caracteristica_tipo.descripcion as "Posee conexión a internet"
from
ra2017.localizacion loc
join ra2017.establecimiento est using (id_establecimiento)
join codigos.ambito_tipo using (c_ambito)
join codigos.sector_tipo using (c_sector)
join ra2017.loc_campo_prov_valor on loc.id_localizacion=loc_campo_prov_valor.id_localizacion
join ra2017.campo_prov using (id_campo_prov)
join
(
select id_localizacion,
localidad_tipo.nombre as localidad,
case
when calle = '' or calle is null then 'No especificado'
else calle
end as calle,
case when nro = '' or nro is null then 'Sin Número'
else 'N° ' || nro
end as nro
from ra2017.domicilio
join ra2017.localizacion_domicilio using (id_domicilio)
join codigos.localidad_tipo using (c_localidad)
where
localizacion_domicilio.c_tipo_dom in (1)
) as domicilio on loc.id_localizacion=domicilio.id_localizacion
left join ra2017.caracteristicas on loc.id_localizacion = caracteristicas.id_localizacion
join codigos.caracteristica_tipo using (c_caracteristica)
where
loc.c_estado in (1,2) -- Filtrado de localizaciones activas/inactivas
and
campo_prov.nombre = 'region'
and
caracteristicas.c_caracteristica in (131, 132)
and
est.cue || loc.anexo ilike 
"""

MATRICULANIVEL = """
select
--est.cue || loc.anexo as "Cueanexo",
--loc.codigo_jurisdiccional as "Nro",
case
when oferta_base_tipo.c_oferta_base in (1,17,86) then 'Inicial'
when oferta_base_tipo.c_oferta_base in (2,40,41,87) then 'Primario'
when oferta_base_tipo.c_oferta_base in (7,42,43,44,45,54,55,58,88,5,111) then 'Secundario'
when oferta_base_tipo.c_oferta_base in (4,47,48,49,50) then 'Superior'
when oferta_base_tipo.c_oferta_base in (21) then 'Adultos-Formación Profesional'
else oferta_base_tipo.descripcion
end as "Nivel",
coalesce(sum(mat_oferta.total_matricula),0) as "Matrícula"
from
ra2017.localizacion loc
join ra2017.establecimiento est using (id_establecimiento)
left join ra2017.oferta_local using (id_localizacion)
join codigos.oferta_tipo using (c_oferta)
join codigos.oferta_base_tipo using (c_oferta_base)
left join (
select id_oferta_local, coalesce(sum(alumnos.total),0) as total_matricula,
coalesce(sum(alumnos.varones),0) as varones, coalesce(sum(alumnos.total - alumnos.varones),0) as mujeres
from
ra2017.alumnos
left join ra2017.plan_dictado using (id_plan_dictado)
left join ra2017.oferta_local using (id_oferta_local)
where
alumnos.c_alumno in (1)
group by 1
) as mat_oferta using (id_oferta_local)
where
loc.c_estado in (1,2) -- Filtrado de localizacion activa/inactiva
and
oferta_local.c_estado in (1,2) -- Filtrado de oferta activas/inactivas
and
oferta_base_tipo.c_oferta_base not in (22,23,27,51,53,110) -- Ofertas que no generan matrícula
and
est.cue || loc.anexo ilike 
"""

FINMATRICULANIVEL = """
group by 1
"""

MATRICULA= """
select
--est.cue || loc.anexo as "Cueanexo",
--loc.codigo_jurisdiccional as "Nro",
mat_oferta.turno as "Turno",
coalesce(sum(mat_oferta.total_matricula),0) "Matrícula"
from
ra2017.localizacion loc
join ra2017.establecimiento est using (id_establecimiento)
left join ra2017.oferta_local using (id_localizacion)
left join (
select id_oferta_local, turno_tipo.descripcion as turno, coalesce(sum(alumnos.total),0) as total_matricula,
coalesce(sum(alumnos.varones),0) as varones, coalesce(sum(alumnos.total - alumnos.varones),0) as mujeres
from
ra2017.alumnos
left join ra2017.plan_dictado using (id_plan_dictado)
left join ra2017.oferta_local using (id_oferta_local)
left join ra2017.seccion using (id_seccion)
join codigos.turno_tipo using (c_turno)
where
alumnos.c_alumno in (1)
group by 1,2
) as mat_oferta using (id_oferta_local)
join codigos.oferta_tipo using (c_oferta)
join codigos.oferta_base_tipo using (c_oferta_base)
where
loc.c_estado in (1,2) -- Filtrado de localizacion activa/inactiva
and
oferta_local.c_estado in (1,2)
and
oferta_base_tipo.c_oferta_base not in (22,23,27,51,53,110) -- Ofertas que no generan matrícula
and
est.cue || loc.anexo ilike 
"""

FINMATRICULATURNO = """
group by 1
"""

CONFECCIONCUADERNILLO = """
select
initcap(confecciono_cuadernillo.nombre || ' ' || confecciono_cuadernillo.apellido) as "Nombre",
lower(confecciono_cuadernillo.email) as "Correo electrónico"
from
ra2017.localizacion loc
join ra2017.establecimiento est using (id_establecimiento)
left join ra2017.confecciono_cuadernillo using (id_localizacion)
where
loc.c_estado in (1,2) -- Filtrado de localizaciones activas/inactivas
and
est.cue || loc.anexo ilike 
"""

RESPONSABLELOC = """
select
initcap(responsable.nombre || ' ' || responsable.apellido) as "Nombre",
lower(responsable.email) as "Correo electrónico"
from
ra2017.localizacion loc
join ra2017.establecimiento est using (id_establecimiento)
left join ra2017.responsable on loc.id_responsable=responsable.id_responsable
where
loc.c_estado in (1,2) -- Filtrado de localizaciones activas/inactivas
and
est.cue || loc.anexo ilike 
"""

INFODIRECTOR = """
select
initcap(responsable.nombre || ' ' || responsable.apellido) as "Nombre",
lower(responsable.email) as "Correo electrónico"
from
ra2017.localizacion loc
join ra2017.establecimiento est using (id_establecimiento)
left join ra2017.responsable on est.id_responsable=responsable.id_responsable
where
loc.c_estado in (1,2) -- Filtrado de localizaciones activas/inactivas
and
est.cue || loc.anexo ilike 
"""

SECCIONESPORNIVEL = """
select
case
when oferta_base_tipo.c_oferta_base in (1,17,86) then 'Inicial'
when oferta_base_tipo.c_oferta_base in (2,40,41,87) then 'Primario'
when oferta_base_tipo.c_oferta_base in (7,42,43,44,45,54,55,58,88,5,111) then 'Secundario'
when oferta_base_tipo.c_oferta_base in (4,47,48,49,50) then 'Superior'
when oferta_base_tipo.c_oferta_base in (21) then 'Adultos-Formación Profesional'
else oferta_base_tipo.descripcion
end as "Nivel",
count (distinct alumnos.id_seccion) as "Cantidad Secciones"
from
ra2017.localizacion loc
join ra2017.establecimiento est using (id_establecimiento)
left join ra2017.oferta_local using (id_localizacion)
left join ra2017.plan_dictado using (id_oferta_local)
join codigos.oferta_tipo using (c_oferta)
join codigos.oferta_base_tipo using (c_oferta_base)
left join ra2017.alumnos using (id_plan_dictado)
left join ra2017.seccion using (id_seccion)
where
loc.c_estado in (1,2)
and
oferta_local.c_estado in (1,2)
and
oferta_base_tipo.c_oferta_base not in (22,23,27,51,53,110) -- Ofertas que no generan matrícula
and
est.cue || loc.anexo ilike 
"""

FINSECCIONESPORNIVEL = """
group by 1
"""

REPITENCIANIVEL = """
select
case
when oferta_base_tipo.c_oferta_base in (1,17,86) then 'Inicial'
when oferta_base_tipo.c_oferta_base in (2,40,41,87) then 'Primario'
when oferta_base_tipo.c_oferta_base in (7,42,43,44,45,54,55,58,88,5,111) then 'Secundario'
when oferta_base_tipo.c_oferta_base in (4,47,48,49,50) then 'Superior'
when oferta_base_tipo.c_oferta_base in (21) then 'Adultos-Formación Profesional'
else oferta_base_tipo.descripcion
end as "Nivel",
coalesce(sum(alumnos.total),0) "Repitencia"
from
ra2017.localizacion loc
join ra2017.establecimiento est using (id_establecimiento)
left join ra2017.oferta_local using (id_localizacion)
left join ra2017.plan_dictado using (id_oferta_local)
join codigos.oferta_tipo using (c_oferta)
join codigos.oferta_base_tipo using (c_oferta_base)
left join ra2017.alumnos using (id_plan_dictado)
where
loc.c_estado in (1,2)
and
oferta_local.c_estado in (1,2)
and
oferta_base_tipo.c_oferta_base not in (22,23,27,51,53,110) -- Ofertas que no generan matrícula
and
alumnos.c_alumno in (2)
and
est.cue || loc.anexo ilike 
"""

FINREPITENCIANIVEL = """
group by 1
"""

EGRESADOSNIVEL = """
select
case
when oferta_base_tipo.c_oferta_base in (1,17,86) and oferta_tipo.c_modalidad1 in (1) then 'Inicial'
when oferta_base_tipo.c_oferta_base in (40,41,87) and oferta_tipo.c_modalidad1 in (1) then 'Primario'
when oferta_base_tipo.c_oferta_base in (42,43,44,45,58,88,5,111,22,23) and oferta_tipo.c_modalidad1 in (1) then 'Secundario'
when oferta_base_tipo.c_oferta_base in (4,47,48,49,50) and oferta_tipo.c_modalidad1 in (1) then 'Superior'
when oferta_base_tipo.c_oferta_base in (2,7,21,54,55) and oferta_tipo.c_modalidad1 in (3) then 'Adultos'
else oferta_base_tipo.descripcion
end as "Nivel",
coalesce(sum(trayectoria.total) filter(where trayectoria.c_trayectoria in (12)),0) as "Egresados",
coalesce(sum(trayectoria.total) filter(where trayectoria.c_trayectoria in (7)),0) as "Promovidos último día de clase",
coalesce(sum(trayectoria.total) filter(where trayectoria.c_trayectoria in (8)),0) as "Promovidos con exámen",
coalesce(sum(trayectoria.total) filter(where trayectoria.c_trayectoria in (9)),0) as "No promovidos"
from
ra2017.localizacion loc
join ra2017.establecimiento est using (id_establecimiento)
left join ra2017.oferta_local using (id_localizacion)
left join ra2017.plan_dictado using (id_oferta_local)
join codigos.oferta_tipo using (c_oferta)
join codigos.oferta_base_tipo using (c_oferta_base)
left join ra2017.trayectoria using (id_plan_dictado)
where
loc.c_estado in (1,2)
and
oferta_local.c_estado in (1,2)
and
oferta_base_tipo.c_oferta_base not in (27,51,53,110) -- Ofertas que no generan egresados
and
est.cue || loc.anexo ilike
"""

FINEGRESADOSNIVEL = """
group by 1
"""

DESERCIONNIVEL = """
select
case
when oferta_base_tipo.c_oferta_base in (1,17,86) and oferta_tipo.c_modalidad1 in (1) then 'Inicial'
when oferta_base_tipo.c_oferta_base in (40,41,87) and oferta_tipo.c_modalidad1 in (1) then 'Primario'
when oferta_base_tipo.c_oferta_base in (42,43,44,45,58,88,5,111,22,23) and oferta_tipo.c_modalidad1 in (1) then 'Secundario'
when oferta_base_tipo.c_oferta_base in (4,47,48,49,50) and oferta_tipo.c_modalidad1 in (1) then 'Superior'
when oferta_base_tipo.c_oferta_base in (2,7,21,54,55) and oferta_tipo.c_modalidad1 in (3) then 'Adultos'
else oferta_base_tipo.descripcion
end as "Nivel",
coalesce(sum(trayectoria.total) filter(where trayectoria.c_trayectoria in (5)),0) as "Deserción"
from
ra2017.localizacion loc
join ra2017.establecimiento est using (id_establecimiento)
left join ra2017.oferta_local using (id_localizacion)
left join ra2017.plan_dictado using (id_oferta_local)
join codigos.oferta_tipo using (c_oferta)
join codigos.oferta_base_tipo using (c_oferta_base)
left join ra2017.trayectoria using (id_plan_dictado)
where
loc.c_estado in (1,2)
and
oferta_local.c_estado in (1,2)
and
oferta_base_tipo.c_oferta_base not in (27,51,53,110) -- Ofertas que no generan egresados
and
est.cue || loc.anexo ilike
"""

FINDESERCIONNIVEL = """
group by 1
"""

INFOACTIVIDADDOCENTE = """
select
coalesce(sum(actividad.total) filter(where c_actividad_docente in (1)),0) as "En actividad",
coalesce(sum(actividad.total) filter(where c_actividad_docente in (3)),0) as "En actividad designados sólo por horas cátedra",
coalesce(sum(actividad.total) filter(where c_actividad_docente in (4)),0) as "En actividad designados por cargo y horas cátedra"
--sum(actividad.total) filter(where c_actividad_docente in (5)) as "Algo"
from
ra2017.localizacion loc
join ra2017.establecimiento est using (id_establecimiento)
left join ra2017.oferta_dictada using (id_localizacion)
left join ra2017.actividad using (id_oferta_dictada)
where
loc.c_estado in (1,2)
and
est.cue || loc.anexo ilike 
"""

INFOCARGOS = """
select
--est.cue || loc.anexo as "Cueanexo",
--loc.codigo_jurisdiccional as "Nro",
coalesce(sum(horas.horas) filter(where c_planta in (5,6)),0) as "Cubiertos",
coalesce(sum(horas.horas) filter(where c_planta in (4)),0) as "Sin cubrir",
coalesce(sum(horas.horas) filter(where c_planta in (8,9,10,11,12)),0) as "Fuera de la Planta Funcional"
from
ra2017.localizacion loc
join ra2017.establecimiento est using (id_establecimiento)
left join ra2017.oferta_dictada using (id_localizacion)
left join ra2017.horas using (id_oferta_dictada)
where
loc.c_estado in (1,2)
and
est.cue || loc.anexo ilike
"""
