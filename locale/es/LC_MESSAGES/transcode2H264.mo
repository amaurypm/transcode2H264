��    1      �  C   ,      8  %   9     _          �     �     �     �     �     �  	   �     �  	   �     �     �  )   �  .        G  �  ^  -   	  �   7  �   �  ^   L  b   �     	  $   	     ?	  v   Z	  {   �	     M
  N   b
     �
  '   �
      �
  ,     �   E  �   �  +   �  \   �     %  #   :     ^     d     z     �  $   �     �     �     �  u  �  0   l  (   �     �     �     �  	   �     �     �     �  	      	   
  
             :  /   I  /   y     �  A  �  9     �   =  �   #  U   �  d   I     �  )   �  #   �  �     �   �     o  O   �  "   �  (     %   +  *   Q  �   |  �   ;  7        V     �  -   �          $     =     S  &   k     �     �     �     "   -                        0   !      )   #                                             +                                        /               	   1       .       (       
   &                      *       ,   %          '      $    
==== Transcoding file {:d}/{:d} ==== 
==== Transcoding finished ====  day   days   file  files  hour   hours   minute   minutes   second   seconds   transcoded OK.
  with errors.
 == There following files were ignored: == == There were errors transcoding the files: == ==== Final report ==== CRF value [default: %(default)s]. Determines the output video quality. Smaller values gives better qualities and bigger file sizes, bigger values result in less quality and smaller file sizes. CRF values should be in the range of 0 to 51. 0 is lossless (and with the biggest file size), 51 is worst possible quality (with the smallest file size) and 18 is visually lossless. Default value results in a nice quality/size ratio. CRF values should be in the range of 0 to 51. Default audio language for MKV files obtained (used only if the original stream languages fail to be determined) [default: %(default)s]. Default subtitle language of soft-subbed subtitles (only used if original subtitle languages fail to be determined) [default: %(default)s]. ERROR: ffmpeg is not installed in your system.
This script can not work properly without it.

 ERROR: mkvtoolnix is not installed in your system.
This script can not work properly without it.

 Exiting OK. File {} is not a proper video file.
 Finding crop dimensions... If set then original video files will be erased after transcoding. WARNING: deleted files can not be easily recovered! Indicates the number of processor cores the script will use. 0 indicates to use as many as possible [default: %(default)s]. Input video file(s). Postfix to be added to newly created H.264 video files [default: %(default)s]. Removing temporary file '{}'. Show program's version number and exit. Show this help message and exit. The number of threads must be 0 or positive. This program transcode video files to H264 and AAC in MKV format. Subtitles, if present, are automatically detected and soft subbed into the corresponding output files. Turn on autocrop function. WARNING: Use with caution as some video files has variable width horizontal (and vertical) black bars, in those cases you will probably lose data. Unknown preset "{}".
Valid values are:
	{}
 WARNING: Deleting file {} as commanded with -r option.
This file won't be easily recovered.
 Work finished in {}. X264 preset [default: %(default)s]. error expected one argument optional arguments positional arguments the following arguments are required too few arguments unrecognized arguments usage Project-Id-Version: PROJECT VERSION
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2017-06-07 15:23-0400
PO-Revision-Date: 2017-06-07 15:33-0400
Last-Translator: 
Language-Team: 
Language: es
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.3.4
X-Generator: Poedit 1.8.12
Plural-Forms: nplurals=2; plural=(n != 1);
 
==== Transcodificando el fichero {:d}/{:d} ==== 
==== Transcodificación finalizada ====  día   días   fichero  ficheros  hora   horas   minuto   minutos   segundo   segundos   bien transcodificado(s).
  con errores.
 == Fueron ignorados los siguientes ficheros: == == Hubo errores con los siguientes ficheros: == ==== Reporte final ==== Valor de CRF [valor por defecto: %(default)s]. Determina la calidad del video de salida. Con valores más pequeños se obtiene mayor calidad, pero con mayor tamaño de fichero, valores grandes resultan en menor calidad y menor tamaño de fichero. Los valores de CRF deben estar en el rango entre 0 y 51. 0 genera un video sin pérdida por compresión (lossless), pero con el mayor tamaño. 51 genera el video con peor calidad (y el menor tamaño) y 18 genera un video sin pérdida aparente de calidad. El valor por defecto genera videos con una buena relación calidad/tamaño. Los valores de CRF deben estar en el rango entre 0 to 51. Lenguaje por defecto de las pistas de audio en los ficheros MKV generados (utilizados solo en caso de que no puedan ser determinados de forma automática los lenguajes originales de estas pistas) [valor por defecto: %(default)s]. Lenguaje por defecto de los subtítulos incluidos en el o los ficheros de salida (utilizado solamente en el caso en que no se pueda determinar el lenguaje de los subtitulos) [valor por defecto: %(default)s]. ERROR: ffmpeg no está instalado en su sistema.
Este script no funciona sin ffmpeg.

 ERROR: mkvtoolnix no está instalado en su sistema.
Este script no puede funcionar sin mkvtoolnix.

 Finalizando OK. El fichero {} no es un archivo de video.
 Buscando dimensiones para cortar... Si se especifica esta opción los videos originales van a ser borrados después de terminada la transcodificación. ALERTA: ¡Los videos borrados no pueden ser recuperados con facilidad! Indica el número de núcleos de procesador que el script va a utilizar. El valor 0 implica utilizar tantos núcleos como sea posible [valor por defecto: %(default)s]. Fichero(s) de video de entrada. Prefijo que se le añade a los ficheros H.264 generados [default: %(default)s]. Borrando el fichero temporal '{}'. Muestra la versión del programa y sale. Muestra este mensaje de ayuda y sale. El número de hilos debe ser 0 o positivo. Este programa transcodifica ficheros de video a H264 y AAC en un formato MKV. Los subtítulos, si hay, son detectados automáticamente e incluidos en los ficheros de salida correspondientes. Enciende la función de recorte automático. ALERTA: Use esta opción con cautela pues algunos videos poseen barras negras horizontales y/o verticales de ancho variable y en estos casos probablemente usted pierda información. preset desconocido "{}".
Los valores válidos son:
	{}
 ADVERTENCIA: Borrado el fichero {} tal como se indicó con la opción -r.
Este fichero no podrá ser recuperado con facilidad.
 Trabajo finalizado en {}. X264 preset [valor por defecto: %(default)s]. error se requiere un argumento argumentos opcionales argumentos posicionales se requieren los siguientes argumentos muy pocos argumentos argumentos no conocidos uso 