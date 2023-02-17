package com.example.CoTEVer.repository

import com.example.CoTEVer.entity.Log
import org.springframework.data.mongodb.repository.MongoRepository
import org.springframework.stereotype.Repository

@Repository
interface LogRepository : MongoRepository<Log, String>