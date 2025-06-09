<?php
/**
 * Configuración personalizada de phpMyAdmin
 */

// Tiempo máximo de ejecución
$cfg['ExecTimeLimit'] = 300;

// Tamaño máximo de subida
$cfg['UploadDir'] = '';
$cfg['SaveDir'] = '';
$cfg['MaxRows'] = 50;

// Configuración de exportación
$cfg['Export']['method'] = 'quick';
$cfg['Export']['charset'] = 'utf-8';

// Configuración de seguridad
$cfg['ShowPhpInfo'] = false;
$cfg['ShowChgPassword'] = true;
$cfg['AllowArbitraryServer'] = false;

// Configuración de la interfaz
$cfg['NavigationTreeEnableGrouping'] = true;
$cfg['MaxNavigationItems'] = 250;
$cfg['NavigationTreeDisplayItemFilterMinimum'] = 30;
$cfg['DefaultLang'] = 'es';
$cfg['DefaultConnectionCollation'] = 'utf8mb4_unicode_ci'; 