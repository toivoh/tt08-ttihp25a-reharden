function (gtry_compileResourceFile)

    set(oneValueArgs "NAMESPACE" "OUTPUT_PREFIX")
    set(multiValueArgs "BINARY_FILES")

	cmake_parse_arguments(GTRY_COMPILERESOURCEFILE "" "${oneValueArgs}" "${multiValueArgs}" ${ARGN} )

	list(JOIN GTRY_COMPILERESOURCEFILE_BINARY_FILES "\;" concatenated_files)

	add_custom_command(
		OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/${GTRY_COMPILERESOURCEFILE_OUTPUT_PREFIX}.h ${CMAKE_CURRENT_BINARY_DIR}/${GTRY_COMPILERESOURCEFILE_OUTPUT_PREFIX}.cpp
		COMMAND ${CMAKE_COMMAND} -DNAMESPACE=${GTRY_COMPILERESOURCEFILE_NAMESPACE} -D SOURCE_DIR=${CMAKE_CURRENT_SOURCE_DIR} -D OUTPUT=${GTRY_COMPILERESOURCEFILE_OUTPUT_PREFIX} -D FILES=${concatenated_files} -P ${CMAKE_CURRENT_FUNCTION_LIST_DIR}/GtryFilesToResourceFile.cmake
		DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/${GTRY_COMPILERESOURCEFILE_BINARY_FILES} ${CMAKE_CURRENT_FUNCTION_LIST_DIR}/GtryFilesToResourceFile.cmake
		VERBATIM)
endfunction()