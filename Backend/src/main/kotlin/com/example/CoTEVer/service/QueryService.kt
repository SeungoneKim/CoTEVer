package com.example.CoTEVer.service

import com.example.CoTEVer.dto.*
import com.example.CoTEVer.repository.LogRepository
import org.springframework.http.MediaType
import org.springframework.stereotype.Service
import org.springframework.web.reactive.function.client.WebClient
import org.springframework.web.reactive.function.client.awaitBody
import org.springframework.web.reactive.function.client.body
import reactor.core.publisher.Mono

@Service
class QueryService(
    val logRepository: LogRepository
) {
    suspend fun getAnswer(questionRequestDto: QuestionRequestDto) : QuestionResponseDto{
        val client = WebClient.create("http://35.206.248.188:5000/test")
        val ret =  client.post()
            .uri("http://35.206.248.188:5000/test")
            .contentType(MediaType.APPLICATION_JSON)
            .body(Mono.just(questionRequestDto))
            .retrieve()
            .awaitBody<QuestionResponseDto>()
        return ret
    }

    fun saveResult(resultRequestDto: ResultRequestDto){
        logRepository.save(resultRequestDto.toLog())
    }
}