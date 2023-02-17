package com.example.CoTEVer.controller

import com.example.CoTEVer.dto.QuestionResponseDto
import com.example.CoTEVer.dto.QuestionRequestDto
import com.example.CoTEVer.dto.ResultRequestDto
import com.example.CoTEVer.service.QueryService
import org.springframework.web.bind.annotation.CrossOrigin
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RestController

@RestController
@CrossOrigin("*")
class ClientController(
    val queryService: QueryService
){
    @PostMapping("/query")
    suspend fun userQuery(@RequestBody questionRequestDto: QuestionRequestDto) : QuestionResponseDto{
        return queryService.getAnswer(questionRequestDto)
    }

    @PostMapping("/result")
    fun userResult(@RequestBody resultRequestDto: ResultRequestDto){
        queryService.saveResult(resultRequestDto)
    }
}