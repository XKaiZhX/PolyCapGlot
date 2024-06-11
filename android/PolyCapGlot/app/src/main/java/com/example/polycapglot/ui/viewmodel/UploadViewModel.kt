package com.example.polycapglot.ui.viewmodel

import android.net.Uri
import android.util.Log
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.polycapglot.services.retrofit.RetrofitInstance
import com.example.polycapglot.services.retrofit.models.UploadRequestData
import com.example.polycapglot.services.retrofit.models.VideoRequestData
import com.google.firebase.ktx.Firebase
import com.google.firebase.storage.ktx.storage
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class UploadViewModel : ViewModel() {

    private val storage = Firebase.storage
    private val storageRef = storage.reference

    // Language lists
    val originalLanguages = listOf("EN", "ES", "AR", "BG", "CS", "DA", "DE", "EL", "ET", "FI", "FR", "HU", "ID", "IT", "JA", "KO", "LT", "LV", "NB", "NL", "PL", "PT", "RO", "RU", "SK", "SL", "SV", "TR", "UK", "ZH")
    val translationLanguages = listOf("AR", "BG", "CS", "DA", "DE", "EL", "EN-GB", "EN-US", "ES", "ET", "FI", "FR", "HU", "ID", "IT", "JA", "KO", "LT", "LV", "NB", "NL", "PL", "PT", "PT-BR", "PT-PT", "RO", "RU", "SK", "SL", "SV", "TR", "UK", "ZH")

    // State variables
    var uploaded by mutableStateOf(0)
    var storageFilename by mutableStateOf("")
    var uri by mutableStateOf<Uri?>(null)

    // Retrofit instance
    private val retrofit = RetrofitInstance()

    //private val apiService = retrofit.create(ApiService::class.java)

    fun prerequestFunction(title: String, originalLanguage: String, translationLanguage: String, token: String, onSuccess: () -> Unit, onError: (Exception) -> Unit) {
        viewModelScope.launch {
            try {
                val requestData = VideoRequestData(title = title, language = originalLanguage)
                val response = withContext(Dispatchers.IO) {
                    retrofit.api.uploadVideoPrerequest(token, requestData)
                }

                if (response.isSuccessful) {
                    response.body()?.let { responseData ->
                        Log.d("UploadViewModel", "Response: token=${responseData.token}, uri=${responseData.uri}")
                        storageFilename = responseData.uri
                        uploadFileFirebase({
                            uploadFileFunction(responseData.video_id, translationLanguage, responseData.token,
                                { onSuccess() }, onError)
                        }, onError)
                    } ?: run {
                        Log.e("UploadViewModel", "Response body is null")
                        onError(Exception("Response body is null"))
                    }
                } else {
                    Log.e("UploadViewModel", "Request failed with status: ${response.code()}")
                    onError(Exception("Request failed with status: ${response.code()}"))
                }
            } catch (e: Exception) {
                Log.e("UploadViewModel", "Request failed", e)
                onError(e)
            }
        }
    }

    fun uploadFileFunction(videoId: String, sub: String, token: String, onSuccess: () -> Unit, onError: (Exception) -> Unit) {
        viewModelScope.launch {
            try {
                val requestData = UploadRequestData(videoId, sub)
                val response = withContext(Dispatchers.IO) {
                    retrofit.api.uploadVideoRequest(token, requestData)
                }

                if (response.isSuccessful) {
                    onSuccess()
                } else {
                    Log.e("UploadViewModel", "Upload request failed with status: ${response.code()}")
                    onError(Exception("Upload request failed with status: ${response.code()}"))
                }
            } catch (e: Exception) {
                Log.e("UploadViewModel", "Upload request failed", e)
                onError(e)
            }
        }
    }

    fun uploadFileFirebase(onSuccess: () -> Unit, onError: (Exception) -> Unit) {
        val videoRef = storageRef.child(storageFilename)
        videoRef.putFile(uri!!)
            .addOnSuccessListener {
                Log.i("FIREBASE", "Uploaded")
                onSuccess()
            }
            .addOnFailureListener { exception ->
                Log.i("FIREBASE", "Not uploaded", exception)
                onError(exception)
            }
    }
}
