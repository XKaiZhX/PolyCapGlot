package com.example.polycapglot.ui.viewmodel

import android.util.Log
import androidx.compose.runtime.MutableState
import androidx.compose.runtime.mutableStateOf
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.polycapglot.services.retrofit.RetrofitInstance
import com.example.polycapglot.services.retrofit.models.LoginData
import com.example.polycapglot.services.retrofit.models.LoginResponse
import com.example.polycapglot.services.retrofit.models.RegisterData
import com.example.polycapglot.services.retrofit.models.UserDataDTO
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class StartSessionViewModel: ViewModel() {
    private val apiService = RetrofitInstance().api
    val response: MutableState<String> = mutableStateOf("")

    suspend fun login(email: String, password: String): LoginResponse?{
        var final: LoginResponse? = null

        val data = LoginData(email, password)
        Log.i("LOGIN", "Login with: ${data}")
        try {
            val res = apiService.login(data);
            Log.i("LOGIN", "Value received is: ${res.body()}")
            if (res.isSuccessful) {
                final = res.body()
            } else {
                Log.i("LOGIN", "Error: " + res.message())
            }
        } catch (e: Exception){
            //TODO: Show user when servers are down
            Log.i("LOGIN", "Exception: " + e.message)
        }
        return final
    }

    suspend fun register(username:String, email: String, password: String): UserDataDTO? {
        var final: UserDataDTO? = null

        val data = RegisterData(username, email, password)
        Log.i("REGISTER", "Register with: ${data}")
        val res = apiService.registerRequest(data);
        if (res.isSuccessful){
            final = res.body()
        }
        Log.i("REGISTER", "Value received is: ${res.body()}")
        return final
    }
}