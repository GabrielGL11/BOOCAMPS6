from django.db import models


class DatosPersonales(models.Model):
    ESTADO_PERFIL = [
        (0, 'Inactivo'),
        (1, 'Activo'),
    ]

    SEXO_CHOICES = [
        ('H', 'Hombre'),
        ('M', 'Mujer'),
    ]

    imagenperfil = models.ImageField(
        upload_to='perfiles/',
        blank=True,
        null=True
    )

    descripcionperfil = models.TextField()
    perfilactivo = models.IntegerField(choices=ESTADO_PERFIL, default=1)
    apellidos = models.CharField(max_length=60)
    nombres = models.CharField(max_length=60)
    nacionalidad = models.CharField(max_length=20)
    lugarnacimiento = models.CharField(max_length=60)
    fechanacimiento = models.DateField()
    numerocedula = models.CharField(max_length=10, unique=True)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    estadocivil = models.CharField(max_length=50)
    licenciaconducir = models.CharField(max_length=6, blank=True, null=True)
    telefonoconvencional = models.CharField(max_length=15, blank=True, null=True)
    telefonofijo = models.CharField(max_length=15, blank=True, null=True)
    direcciontrabajo = models.CharField(max_length=50, blank=True, null=True)
    direcciondomiciliaria = models.CharField(max_length=50)
    sitioweb = models.CharField(max_length=60, blank=True, null=True)

    class Meta:
        db_table = "DATOSPERSONALES"

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"


class ExperienciaLaboral(models.Model):
    perfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)
    cargodesempenado = models.CharField(max_length=100)
    nombrempresa = models.CharField(max_length=50)
    lugarempresa = models.CharField(max_length=50)
    emailempresa = models.EmailField(max_length=100, blank=True, null=True)
    sitiowebempresa = models.CharField(max_length=100, blank=True, null=True)
    nombrecontactoempresarial = models.CharField(max_length=100)
    telefonocontactoempresarial = models.CharField(max_length=60)
    fechainiciogestion = models.DateField()
    fechafingestion = models.DateField(blank=True, null=True)
    descripcionfunciones = models.TextField()
    activarparaqueseveaenfront = models.BooleanField(default=True)
    rutacertificado = models.FileField(
    upload_to='certificados/',
    blank=True,
    null=True
)


    class Meta:
        db_table = "EXPERIENCIALABORAL"

    def __str__(self):
        return f"{self.cargodesempenado} - {self.nombrempresa}"


class Reconocimientos(models.Model):
    TIPOS_RECONOCIMIENTO = [
        ('Académico', 'Académico'),
        ('Público', 'Público'),
        ('Privado', 'Privado'),
    ]

    perfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)
    tiporeconocimiento = models.CharField(max_length=100, choices=TIPOS_RECONOCIMIENTO)
    fechareconocimiento = models.DateField()
    descripcionreconocimiento = models.TextField()
    entidadpatrocinadora = models.CharField(max_length=100)
    nombrecontactoauspicia = models.CharField(max_length=100)
    telefonocontactoauspicia = models.CharField(max_length=60)
    activarparaqueseveaenfront = models.BooleanField(default=True)
    rutacertificado = models.FileField(
    upload_to='certificados/',
    blank=True,
    null=True
)


    class Meta:
        db_table = "RECONOCIMIENTOS"

    def __str__(self):
        return f"{self.tiporeconocimiento} - {self.perfil.nombres}"


class CursosRealizados(models.Model):
    perfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)
    nombrecurso = models.CharField(max_length=100)
    fechainicio = models.DateField()
    fechafin = models.DateField()
    totalhoras = models.DecimalField(max_digits=6, decimal_places=2)
    descripcioncurso = models.TextField()
    entidadpatrocinadora = models.CharField(max_length=100)
    nombrecontactoauspicia = models.CharField(max_length=100)
    telefonocontactoauspicia = models.CharField(max_length=60)
    emailempresapatrocinadora = models.EmailField(max_length=60, blank=True, null=True)
    activarparaqueseveaenfront = models.BooleanField(default=True)
    rutacertificado = models.FileField(
    upload_to='certificados/',
    blank=True,
    null=True
)


    class Meta:
        db_table = "CURSOSREALIZADOS"

    def __str__(self):
        return f"{self.nombrecurso} - {self.perfil.nombres}"


class ProductosAcademicos(models.Model):
    perfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)
    nombrerecurso = models.CharField(max_length=100)
    clasificador = models.CharField(max_length=100)
    descripcion = models.TextField()
    activarparaqueseveaenfront = models.BooleanField(default=True)

    class Meta:
        db_table = "PRODUCTOSACADEMICOS"

    def __str__(self):
        return self.nombrerecurso


class ProductosLaborales(models.Model):
    perfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)
    nombreproducto = models.CharField(max_length=100)
    fechaproducto = models.DateField()
    descripcion = models.TextField()
    activarparaqueseveaenfront = models.BooleanField(default=True)

    class Meta:
        db_table = "PRODUCTOSLABORALES"

    def __str__(self):
        return self.nombreproducto


class VentaGarage(models.Model):
    ESTADOS_PRODUCTO = [
        ('Bueno', 'Bueno'),
        ('Regular', 'Regular'),
    ]

    perfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)
    nombreproducto = models.CharField(max_length=100)
    estadoproducto = models.CharField(max_length=40, choices=ESTADOS_PRODUCTO)
    descripcion = models.TextField()
    valordelbien = models.DecimalField(max_digits=5, decimal_places=2)
    activarparaqueseveaenfront = models.BooleanField(default=True)

    class Meta:
        db_table = "VENTAGARAGE"

    def __str__(self):
        return self.nombreproducto
