package com.example.polycapglot.services.retrofit

import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.create

class RetrofitInstance(/*serverIp: String?*/) {
    private val BASE_URL = "http://192.168.1.49:9002/" //serverIp
    val api: ApiService by lazy {
        val retrofit = BASE_URL.let {
            Retrofit.Builder()
                .baseUrl(it)
                .addConverterFactory(GsonConverterFactory.create())
                .build()
        }
        retrofit.create(ApiService::class.java)
    }
}