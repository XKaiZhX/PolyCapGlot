package com.example.polycapglot.ui.viewmodel

import android.util.Log
import androidx.compose.runtime.MutableState
import androidx.compose.runtime.mutableStateOf
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.polycapglot.services.retrofit.RetrofitInstance
import com.example.polycapglot.services.retrofit.models.LoginData
import kotlinx.coroutines.launch
import java.lang.Exception

class RetrofitViewModel: ViewModel() {
    private val apiService = RetrofitInstance().api
    val response: MutableState<String> = mutableStateOf("")

    fun testApi(){
        viewModelScope.launch {
            try {
                Log.i("RETROFIT", "Sending request to http://192.168.1.49:9002/android")
                val res = apiService.testRequest()
                if(res.isNotEmpty())
                    response.value = res
            } catch (e: Exception) {
                Log.i("RETROFIT", "Unknown error: " + e.message)
            }
        }
    }
}