package com.example.polycapglot.ui.viewmodel

import android.app.Application
import android.graphics.Bitmap
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.arthenica.mobileffmpeg.Config
import com.arthenica.mobileffmpeg.FFmpeg
import com.bumptech.glide.Glide
import com.bumptech.glide.request.FutureTarget
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.io.File

class HomeViewModel(application: Application) : AndroidViewModel(application) {
    var thumbnail = mutableStateOf<Bitmap?>(null)
        private set

    fun generateThumbnail(videoUrl: String) {
        viewModelScope.launch {
            thumbnail.value = generateThumbnailInternal(videoUrl)
        }
    }

    private suspend fun generateThumbnailInternal(videoUrl: String): Bitmap? {
        return withContext(Dispatchers.IO) {
            try {
                val file = File(getApplication<Application>().cacheDir, "video_thumbnail.jpg")
                val command = arrayOf(
                    "-y",
                    "-i", videoUrl,
                    "-ss", "00:00:01",
                    "-vframes", "1",
                    file.absolutePath
                )
                val rc = FFmpeg.execute(command)
                if (rc == Config.RETURN_CODE_SUCCESS) {
                    val futureTarget: FutureTarget<Bitmap> = Glide.with(getApplication<Application>())
                        .asBitmap()
                        .load(file)
                        .submit()
                    futureTarget.get()
                } else {
                    null
                }
            } catch (e: Exception) {
                e.printStackTrace()
                null
            }
        }
    }
}