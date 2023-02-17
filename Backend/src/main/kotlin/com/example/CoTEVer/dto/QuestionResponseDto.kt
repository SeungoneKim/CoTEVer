package com.example.CoTEVer.dto

data class QuestionResponseDto(
    val question:String,
    val explanation:Map<Int, ApiNode>,
    val output:ApiOutput
)

data class ApiNode(
    val sub_question:String,
    val sub_answer:String,
    val evidence_document:Map<Int, Document>
)

data class Document(
    val url : String,
    val title : String,
    val document : String,
    val score : Float
)

data class ApiOutput(
    //val final_explanation:String,
    val final_answer:String,
)