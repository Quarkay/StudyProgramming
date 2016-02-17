<?php

/**
 * Data: 2016.02
 * Author: 一把杀猪刀 blog: www.mierhuo.com
 */

include('MemcachedProxy.php');

$mem = new MemcachedProxy();

$mem->get('a');
$mem->add('b',array('a'=>0),0);
$mem->delete('b');
$mem->get('d');
$mem->get('e');