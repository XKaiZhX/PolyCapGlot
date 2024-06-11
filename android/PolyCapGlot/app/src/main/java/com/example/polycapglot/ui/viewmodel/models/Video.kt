package com.example.polycapglot.ui.viewmodel.models

data class Video(
    val id: String,
    val title: String,
    val language: String,
    val firebase_uri: String,
    val translations: List<Translation>
)
