package com.example.CoTEVer.entity

import com.example.CoTEVer.dto.ResultRequestDto
import org.springframework.data.mongodb.core.mapping.Document

@Document(collection = "cotever")
data class Log(
    val resultRequestDto: ResultRequestDto
) {
}