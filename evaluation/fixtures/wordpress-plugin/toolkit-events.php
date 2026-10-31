<?php
/**
 * Plugin Name: Toolkit Community Sessions
 * Description: A read-only community session shortcode used for toolkit outcome evaluation.
 * Version: 1.0.0
 * License: GPL-2.0-or-later
 */
defined('ABSPATH') || exit;

add_shortcode('toolkit_sessions', function ($attributes) {
    $attributes = shortcode_atts(['heading' => 'Your next good afternoon'], $attributes, 'toolkit_sessions');
    $items = ['Sketch & share', 'A neighborhood lunch', 'Riverside walking club'];
    $html = '<section class="toolkit-sessions" aria-label="Community sessions"><p>GOOD COMPANY / RIGHT HERE</p><h2>' . esc_html($attributes['heading']) . '</h2><ul>';
    foreach ($items as $item) {
        $html .= '<li><h3>' . esc_html($item) . '</h3><p>Meet the neighbors. Try something new.</p></li>';
    }
    return $html . '</ul></section>';
});

add_action('wp_enqueue_scripts', function () {
    wp_register_style('toolkit-sessions', false, [], '1.0.0');
    wp_enqueue_style('toolkit-sessions');
    wp_add_inline_style('toolkit-sessions', '.toolkit-sessions{color:#192a22;background:#f5f3cb;padding:clamp(20px,4vw,48px);border:2px solid #192a22;border-radius:24px;font:17px/1.6 sans-serif}.toolkit-sessions>p{font-size:12px;letter-spacing:.15em;font-weight:bold}.toolkit-sessions h2{font-size:clamp(34px,5vw,60px);line-height:1.05;letter-spacing:-.04em;max-width:600px}.toolkit-sessions ul{list-style:none;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}.toolkit-sessions li{border:2px solid #192a22;border-radius:16px;padding:24px;background:#dda6cd}.toolkit-sessions li:nth-child(2){background:#b8d9c5}.toolkit-sessions li:nth-child(3){background:#f3b773}.toolkit-sessions h3{font-size:24px;line-height:1.2}@media(max-width:650px){.toolkit-sessions ul{grid-template-columns:1fr}}');
});
