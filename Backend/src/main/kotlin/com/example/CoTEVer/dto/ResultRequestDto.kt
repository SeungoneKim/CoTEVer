package com.example.CoTEVer.dto

import com.example.CoTEVer.entity.Log

data class ResultRequestDto(
    val query : String,
    val stepCount : Int,
    val finalAnswer : String,
    val finalAnswerAlt : String,
    val finalAnswerRating : Int,
    val finalExplanation : String,
    val finalExplanationAlt : String,
    val finalExplanationRating : Int,
    val nodeList: List<ResultNode>
) {
    fun toLog() : Log{
        return Log(
            resultRequestDto = this
        )
    }
}

data class ResultNode(
    val subQuestion : String,
    val subQuestionKeyword : String,
    val subAnswer : String,
    val subAnswerRating : Int,
    val subAnswerAlt : String,
    val top5List : List<Pair<String, String>>,
)