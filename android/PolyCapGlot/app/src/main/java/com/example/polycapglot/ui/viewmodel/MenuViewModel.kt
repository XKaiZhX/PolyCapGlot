package com.example.polycapglot.ui.viewmodel

import android.app.Application
import android.graphics.Bitmap
import android.net.Uri
import android.util.Log
import androidx.compose.runtime.mutableStateOf
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.arthenica.mobileffmpeg.Config
import com.arthenica.mobileffmpeg.FFmpeg
import com.bumptech.glide.Glide
import com.bumptech.glide.request.FutureTarget
import com.example.polycapglot.services.retrofit.RetrofitInstance
import com.example.polycapglot.ui.viewmodel.models.Translation
import com.example.polycapglot.ui.viewmodel.models.Video
import com.google.android.gms.tasks.Task
import com.google.android.gms.tasks.Tasks
import com.google.firebase.ktx.Firebase
import com.google.firebase.storage.ktx.storage
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.io.File

class MenuViewModel(
    private val username: String,
    private val email: String,
    val token: String,
    application: Application
) : AndroidViewModel(application) {

    private val retrofitInstance = RetrofitInstance()
    val storage = Firebase.storage
    var videos = mutableStateOf<List<Video>>(emptyList())
        private set

    var videoDownloadLinks = mutableStateOf<List<String>>(emptyList())
        private set

    // Function to request videos
    suspend fun requestVideos(){
        val list = try {
            // Call the Retrofit API to request videos
            val response = retrofitInstance.api.videosRequest(token)
            if (response.isSuccessful) {
                Log.i("VIDEO_REQ", "res: " + response.body().toString())
                response.body() ?: emptyList()
            } else {
                // Handle unsuccessful response
                Log.i("VIDEO_REQ", "res: " + response.errorBody())
                emptyList()
            }
        } catch (e: Exception) {
            // Handle exceptions
            Log.i("VIDEO_REQ", "res: " + e.message)
            emptyList()
        }

        videos.value = list
    }

    fun deleteTranslation(translation: Translation) {
        Log.i("DELETE", "Translation deleted: ${translation.sub_language}")
    }

    fun deleteVideo(video: Video) {
        Log.i("DELETE", "Video deleted: ${video.title}")
    }

    fun requestVideosMock() {
        // TODO: Implement this function to request videos
        val list: MutableList<Video> = mutableListOf(
            Video(
                "Test",
                "ES",
                "raw_videos/89e9ef8b4bf33ac8b2db9d8d4dc110cad363adec28019db0b2a5ad6a21a04f60.mp4",
                listOf(
                    Translation(
                        "EN-US",
                        "translated_videos/f3807e1e02cae3a996d8a792d5559fa868232ff79e02f7fc00a03780b28325ca.mp4",
                        1
                    ),
                    Translation(
                        "FR",
                        "translated_videos/1a3f78d45d33560951d64e508569c4f1bdb1b3dd7aa6b1dafd2a8f17b5d80521.mp4",
                        1
                    ),
                    Translation(
                        "PT-PT",
                        "translated_videos/90667fa1b6355c503d6405823060f8e06e82c57b4ded19e7de7c4c836fbc29b2.mp4",
                        1
                    ),
                    Translation(
                        "RO",
                        "translated_videos/8b1667866d0a42da15d2578e353f0193d59d5ddb3c7d373f285caf991c0d5243.mp4",
                        1
                    ),
                )
            )
        )

        videos.value = list
    }

    fun getDownloadLinks(videoUris: List<String>, callback: (List<String>) -> Unit) {
        val downloadLinks = mutableListOf<String>()
        val tasks = mutableListOf<Task<Uri>>()

        // Iterate through each video URI and get its download link
        for (uri in videoUris) {
            val storageRef = storage.reference.child(uri)
            val task = storageRef.downloadUrl
            tasks.add(task)
        }

        // Wait for all tasks to complete
        Tasks.whenAllComplete(tasks).addOnCompleteListener { taskList ->
            // Iterate through the completed tasks and extract download links
            for (result in taskList.result) {
                if (result.isSuccessful) {
                    val uri = result.result as Uri
                    downloadLinks.add(uri.toString())
                } else {
                    // Handle failure
                    // Log.e(TAG, "Error getting download URL", result.exception)
                }
            }
            // Call the callback function with the list of download links
            callback(downloadLinks)
            videoDownloadLinks.value = downloadLinks
        }

        // Log the download links
        for (link in videoDownloadLinks.value) {
            Log.i("DOWNLOAD_LINK", link)
        }
    }
    fun generateThumbnails(videoUrls: List<String>) {
        viewModelScope.launch {
            thumbnails.value = generateThumbnailsInternal(videoUrls)
        }
    }

    private suspend fun generateThumbnailsInternal(videoUrls: List<String>): List<Bitmap?> {
        return withContext(Dispatchers.IO) {
            val generatedThumbnails = mutableListOf<Bitmap?>()
            try {
                for (videoUrl in videoUrls) {
                    val thumbnail = generateThumbnailInternal(videoUrl)
                    generatedThumbnails.add(thumbnail)
                }
            } catch (e: Exception) {
                e.printStackTrace()
            }
            generatedThumbnails
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

    var thumbnails = mutableStateOf<List<Bitmap?>>(emptyList())
        private set
}