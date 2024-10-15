<script setup>
import { ref, defineExpose } from 'vue'
const props = defineProps(['title', 'isDisabled', 'originalImgFile'])
const emit = defineEmits(['disableEdge', 'enableEdge'])
const responseImg = ref(null) // Variable to store the thumbnail Data URL
const loading = ref(false)
const submitImage = (event) => {
    loading.value = true
    console.log(props.originalImgFile)
    emit('disableEdge')
    setTimeout(() => {
        loading.value = false
        emit('enableEdge')
        const reader = new FileReader()
        reader.onload = (e) => {
            responseImg.value = e.target.result // Store the Data URL for thumbnail preview
        }
        reader.readAsDataURL(props.originalImgFile)
    }, 3000)
}
const previewImage = (event) => {
    const file = event.target.files[0]
    if (file) {
        selectedFile.value = file // Store the selected file
        const reader = new FileReader()
        reader.onload = (e) => {
            thumbnail.value = e.target.result // Store the Data URL for thumbnail preview
        }
        reader.readAsDataURL(file)
    }
}
// defineExpose({
//     selectedFile,
// })
</script>
<template>
    <div class="submit-card">
        <div class="title-section">
            <h1 class="title">{{ title }}</h1>
            <button :disabled="isDisabled" @click="submitImage">Submit</button>
        </div>
        <div class="card">
            <div class="thumbnail-preview">
                <img
                    v-if="!loading"
                    :src="responseImg"
                    alt="Response Image"
                    class="thumbnail"
                />
                <div v-else>Loading...</div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.submit-card {
    width: 300px;
    height: 300px;
    margin: 20px;
    padding: 20px;
    text-align: center;
    border: 1px solid #ddd;
    border-radius: 8px;
    background-color: #f9f9f9;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.title-section {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
}

.title {
    padding: 0 20px;
    font-size: 24px;
    color: #333;
}

.card {
    padding: 20px;
}

.thumbnail-preview {
    margin-top: 20px;
}

.thumbnail {
    max-width: 100%;
    height: auto;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}
</style>
